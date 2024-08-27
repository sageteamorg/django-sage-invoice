from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse


@admin.action(description="Show selected invoice")
def show_invoice(modeladmin, request, queryset):
    invoice = queryset.first()
    if invoice:
        url = reverse("invoice_detail", kwargs={"invoice_slug": invoice.slug})
        return redirect(url)
