from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from sage_invoice.models import InvoiceCategory


@admin.register(InvoiceCategory)
class InvoiceCategoryAdmin(admin.ModelAdmin):
    admin_priority = 2
    list_display = ("title", "description")
    search_fields = ("title", "description")
    readonly_fields = ("slug",)
    ordering = ("title",)
    save_on_top = True

    fieldsets = (
        (
            _("Category Details"),
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                ),
                "description": _(
                    "Details of the invoice category including title and description."
                ),
            },
        ),
    )
