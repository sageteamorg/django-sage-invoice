from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from sage_invoice.admin.actions import show_invoice
from sage_invoice.models import Expense, Invoice, InvoiceColumn, InvoiceItem
from sage_invoice.resource import InvoiceResource


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    min_num = 1
    readonly_fields = ("total_price",)


class InvoiceColumnInline(admin.TabularInline):
    model = InvoiceColumn
    extra = 1


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 1
    readonly_fields = ("subtotal", "tax_amount", "discount_amount", "total_amount")


@admin.register(Invoice)
class InvoiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = InvoiceResource
    admin_priority = 1
    list_display = ("title", "invoice_date", "customer_name", "status")
    search_fields = ("customer_name", "status", "customer_email")
    autocomplete_fields = ("category",)
    save_on_top = True
    list_filter = ("status", "invoice_date", "category")
    ordering = ("-invoice_date",)
    readonly_fields = ("slug",)
    actions = [show_invoice]

    class Media:
        js = ("assets/js/invoice_admin.js",)

    def get_fieldsets(self, request, obj=None):
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
                        "receipt",
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
        )
        fieldsets += (
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

        return fieldsets

    inlines = [InvoiceItemInline, InvoiceColumnInline, ExpenseInline]

    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj and obj.pk:
            inlines = [
                InvoiceItemInline(self.model, self.admin_site),
                InvoiceColumnInline(self.model, self.admin_site),
                ExpenseInline(self.model, self.admin_site),
            ]
        else:
            inlines = [
                InvoiceItemInline(self.model, self.admin_site),
                ExpenseInline(self.model, self.admin_site),
            ]
        return inlines
