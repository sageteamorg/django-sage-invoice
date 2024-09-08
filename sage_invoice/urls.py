from django.urls import path

from sage_invoice.views.invoice import InvoiceDetailView, TemplateChoiceView

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
]
