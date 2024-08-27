from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sage_invoice.admin.actions import export_as_html, show_invoice
from sage_invoice.models import Invoice, InvoiceColumn, InvoiceItem, InvoiceTotal


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ("total_price",)


class InvoiceColumnInline(admin.TabularInline):
    model = InvoiceColumn
    extra = 1


class InvoiceTotalInline(admin.TabularInline):
    model = InvoiceTotal
    extra = 1
    readonly_fields = ("subtotal", "tax_amount", "discount_amount", "total_amount")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    admin_priority = 1
    list_display = ("title", "invoice_date", "customer_name", "status")
    search_fields = ("customer_name", "status", "customer_email")
    autocomplete_fields = ("category",)
    save_on_top = True
    list_filter = ("status", "invoice_date", "category")
    ordering = ("-invoice_date",)
    readonly_fields = ("slug",)
    actions = [export_as_html, show_invoice]

    fieldsets = (
        (
            _("Invoice Details"),
            {
                "fields": (
                    "title",
                    "slug",
                    "invoice_date",
                    "tracking_code",
                    "due_date",
                    "customer_name",
                    "customer_email",
                    "category",
                ),
                "description": _(
                    "Basic details of the invoice including title, date, and customer information."
                ),
            },
        ),
        (
            _("Status & Notes"),
            {
                "fields": ("status", "notes"),
                "description": _(
                    "Current status of the invoice and any additional notes."
                ),
            },
        ),
        (
            _("Design Elements"),
            {
                "fields": (
                    "logo",
                    "signature",
                    "stamp",
                    "template_choice",
                ),
                "description": _(
                    "Design-related elements like logo, and template choice."
                ),
            },
        ),
    )

    inlines = [InvoiceItemInline, InvoiceColumnInline, InvoiceTotalInline]

    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj and obj.pk:
            inlines = [
                InvoiceItemInline(self.model, self.admin_site),
                InvoiceColumnInline(self.model, self.admin_site),
                InvoiceTotalInline(self.model, self.admin_site),
            ]
        else:
            inlines = [
                InvoiceItemInline(self.model, self.admin_site),
                InvoiceTotalInline(self.model, self.admin_site),
            ]
        return inlines
