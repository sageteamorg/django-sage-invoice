from django.db import models
from django.utils.translation import gettext_lazy as _


class InvoiceColumn(models.Model):
    priority = models.PositiveIntegerField(
        verbose_name=_("Priority"),
        help_text=_("The priority associated with each custom column."),
        db_comment="Priority of the column",
    )
    column_name = models.CharField(
        max_length=255,
        verbose_name=_("Column Name"),
        help_text=_(
            "The name of the custom column (e.g., 'Delivery Date', 'Warranty Period')."
        ),
        db_comment="Name of the custom column",
    )
    value = models.TextField(
        verbose_name=_("Value"),
        help_text=_("The value for the custom column in the specific invoice."),
        db_comment="Value of the custom column",
    )
    invoice = models.ForeignKey(
        "Invoice",
        on_delete=models.CASCADE,
        related_name="columns",
        verbose_name=_("Invoice"),
        help_text=_("The invoice associated with this custom column."),
        db_comment="invoice of the custom column",
    )
    item = models.ForeignKey(
        "InvoiceItem",
        on_delete=models.CASCADE,
        related_name="columns",
        verbose_name=_("Item"),
        help_text=_("The item associated with this custom column."),
        db_comment="item of the custom column",
    )

    def __str__(self):
        return f"{self.column_name}"

    def __repr__(self) -> str:
        return f"Invoice Column> {self.column_name}"

    class Meta:
        verbose_name = _("Invoice Column")
        verbose_name_plural = _("Invoice Columns")
        db_table = "sage_invoice_columns"
        ordering = ["priority"]
