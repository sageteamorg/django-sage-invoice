from django.urls import path

from sage_invoice.views.invoice import (
    DownloadInvoicesView,
    GenerateInvoicesView,
    InvoiceDetailView,
    TemplateChoiceView,
)

urlpatterns = [
    path(
        "invoice/<slug:slug>/",
        InvoiceDetailView.as_view(),
        name="invoice_detail",
    ),
    path(
        "template-choices/<str:check>",
        TemplateChoiceView.as_view(),
        name="template_choices",
    ),
    path("generate-pdfs/", GenerateInvoicesView.as_view(), name="generate_pdfs"),
    path(
        "download-invoices/", DownloadInvoicesView.as_view(), name="download_invoices"
    ),
]
