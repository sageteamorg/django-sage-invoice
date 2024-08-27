from django.views.generic import TemplateView

from sage_invoice.models import Invoice
from sage_invoice.service.invoice_create import QuotationService


class InvoiceDetailView(TemplateView):
    template_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_slug = self.kwargs.get("invoice_slug")
        invoice = Invoice.objects.filter(slug=invoice_slug)
        service = QuotationService()
        rendered_content = service.render_contax(invoice)
        context.update(rendered_content)
        self.template_name = f"quotation{invoice.first().template_choice}.html"
        return context
