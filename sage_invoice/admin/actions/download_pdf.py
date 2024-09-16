from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse


@admin.action(description="Download selected invoice as PDF")
def export_pdf(modeladmin, request, queryset):
    invoice_ids = queryset.values_list("id", flat=True)
    invoice_ids_str = ",".join(map(str, invoice_ids))
    url = f"{reverse('download_invoices')}?invoice_ids={invoice_ids_str}"
    return redirect(url)
