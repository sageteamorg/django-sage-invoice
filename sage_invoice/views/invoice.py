from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from sage_invoice.helpers.funcs import get_template_choices
from sage_invoice.models import Invoice
from sage_invoice.service.invoice_create import QuotationService


class InvoiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Invoice
    context_object_name = "invoice"
    queryset = Invoice.objects.select_related("category", "expense").prefetch_related("items", "columns")

    def test_func(self):
        # Ensure that the user is a staff member
        return self.request.user.is_staff

    def handle_no_permission(self):
        # If the user is not authenticated, it will redirect to login
        # If the user is authenticated but lacks permission, it raises PermissionDenied
        if self.request.user.is_authenticated:
            raise PermissionDenied(self.permission_denied_message)
        return super().handle_no_permission()

    def get_template_names(self):
        # Dynamically select the template based on the invoice type
        invoice = self.get_object()
        return [f"{invoice.template_choice}.html"]

    def get_context_data(self, **kwargs):
        # Add additional context using the service class
        context = super().get_context_data(**kwargs)
        invoice = self.get_object()
        context["customer_email"] = invoice.contacts.get("Contact Info").get("email", None)
        context["customer_phone"] = invoice.contacts.get("Contact Info").get("phone", None)
        return context


class TemplateChoiceView(View):
    def get(self, request, *args, **kwargs):
        is_receipt = self.kwargs.get("check")
        if "T" in is_receipt:
            is_receipt = True
        else:
            is_receipt = False
        choices = get_template_choices(is_receipt=is_receipt)
        formatted_choices = [
            {"value": choice[0], "label": choice[1]} for choice in choices
        ]
        return JsonResponse(formatted_choices, safe=False)


class GenerateInvoicesView(TemplateView):
    """
    This view generates multiple invoices and returns their rendered HTML for PDF
    generation.
    """

    def get(self, request, *args, **kwargs):
        invoice_ids = request.GET.get("invoice_ids", "")
        invoice_ids = invoice_ids.split(",") if invoice_ids else []

        if not invoice_ids:
            return JsonResponse({"error": "No invoice IDs provided"}, status=400)

        invoices_data = []

        for invoice_id in invoice_ids:
            invoice = Invoice.objects.filter(id=invoice_id).first()
            if not invoice:
                continue

            service = QuotationService()
            rendered_content = service.render_context(invoice)

            # Determine the template based on invoice type
            if invoice.receipt:
                template_name = f"receipt{invoice.template_choice}.html"
            else:
                template_name = f"quotation{invoice.template_choice}.html"

            rendered_html = render_to_string(template_name, rendered_content)

            invoices_data.append(
                {
                    "id": invoice.id,
                    "title": invoice.title or f"Invoice_{invoice.id}",
                    "rendered_html": rendered_html,
                }
            )

        return JsonResponse({"invoices": invoices_data})


class DownloadInvoicesView(View):
    def get(self, request, *args, **kwargs):
        # Get the invoice IDs from the query parameters
        invoice_ids = request.GET.get("invoice_ids", "")

        context = {"invoice_ids": invoice_ids}

        return render(request, "download_invoices.html", context)
