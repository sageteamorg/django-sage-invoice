from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from sage_invoice.admin.actions import export_pdf
from sage_invoice.models import Column, Expense, Invoice, Item, CustomerProfile
from sage_invoice.resource import InvoiceResource


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    min_num = 1
    readonly_fields = ("total_price",)


class ColumnInline(admin.StackedInline):
    model = Column
    extra = 1


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 1
    readonly_fields = (
        "subtotal",
        "tax_amount",
        "discount_amount",
        "total_amount",
        "concession_amount",
    )


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile


@admin.register(Invoice)
class InvoiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = InvoiceResource
    admin_priority = 1
    list_display = ("title", "invoice_date", "status")
    search_fields = ("status", "customer_email")
    save_on_top = True
    list_filter = ("status", "invoice_date", "category")
    ordering = ("-invoice_date",)
    autocomplete_fields = ("category",)
    readonly_fields = ("slug",)
    actions = [export_pdf]
    inlines = [
        CustomerProfileInline,
        ItemInline,
        ColumnInline,
        ExpenseInline,
    ]

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
                        "category",
                        "receipt",
                    ),
                    "description": _(
                        """
                        Basic details of the invoice including title, date,
                        and customer information."""
                    ),
                },
            ),
            (
                _("Status & Currency"),
                {
                    "fields": ("status", "notes", "currency"),
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

    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj and obj.pk:
            inlines = [
                CustomerProfileInline(self.model, self.admin_site),
                ItemInline(self.model, self.admin_site),
                ColumnInline(self.model, self.admin_site),
                ExpenseInline(self.model, self.admin_site),
            ]
        else:
            inlines = [
                CustomerProfileInline(self.model, self.admin_site),
                ItemInline(self.model, self.admin_site),
                ExpenseInline(self.model, self.admin_site),
            ]
        return inlines
