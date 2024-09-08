from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from sage_invoice.helpers.funcs import get_template_choices
from sage_invoice.models import Invoice
from sage_invoice.service.invoice_create import QuotationService


class InvoiceDetailView(TemplateView):
    template_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_slug = self.kwargs.get("slug")
        invoice = Invoice.objects.filter(slug=invoice_slug)
        service = QuotationService()
        rendered_content = service.render_contax(invoice)
        context.update(rendered_content)
        if invoice.first().receipt:
            self.template_name = f"receipt{invoice.first().template_choice}.html"
        else:
            self.template_name = f"quotation{invoice.first().template_choice}.html"
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
