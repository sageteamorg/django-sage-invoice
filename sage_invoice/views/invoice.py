from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

from sage_invoice.helpers.funcs import get_template_choices
from sage_invoice.models import Invoice
from sage_invoice.service.invoice_create import QuotationService


class InvoiceDetailView(LoginRequiredMixin, TemplateView):
    template_name = ""
    permission_denied_message = (
        "No access - You do not have permission to view this page."
    )

    # Define where to redirect the user if not authenticated
    login_url = "admin/login/"  # Replace with your actual login URL

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is staff before rendering the page
        if not request.user.is_staff:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_slug = self.kwargs.get("slug")
        invoice = Invoice.objects.filter(slug=invoice_slug).first()
        service = QuotationService()
        rendered_content = service.render_context(invoice)
        context.update(rendered_content)

        # Dynamically choose the template based on invoice type and choice
        if invoice.receipt:
            self.template_name = f"{invoice.template_choice}.html"
        else:
            self.template_name = f"{invoice.template_choice}.html"

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
