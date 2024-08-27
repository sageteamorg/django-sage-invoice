from django.urls import path

from sage_invoice.views.invoice import InvoiceDetailView

urlpatterns = [
    path(
        "invoice/<str:invoice_slug>/",
        InvoiceDetailView.as_view(),
        name="invoice_detail",
    ),
]
