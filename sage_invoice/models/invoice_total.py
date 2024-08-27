from django.db import models
from django.utils.translation import gettext_lazy as _

from sage_invoice.service.total import InvoiceTotalService


class InvoiceTotal(models.Model):
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Subtotal"),
        help_text=_("The sum of all item totals."),
        db_comment="Sum of all item totals in the invoice",
    )
    tax_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Tax Percentage"),
        help_text=_("The tax percentage applied to the invoice."),
        db_comment="The percentage of tax applied to the invoice",
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Discount Percentage"),
        help_text=_("The discount percentage applied to the invoice."),
        db_comment="The percentage of discount applied to the invoice",
    )
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Tax Amount"),
        help_text=_("The calculated tax amount."),
        db_comment="The total tax amount calculated based on the subtotal and tax percentage",
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Discount Amount"),
        help_text=_("The calculated discount amount."),
        db_comment="The total discount amount calculated based on the subtotal and discount percentage",
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total Amount"),
        help_text=_("The final total after applying tax and discount."),
        db_comment="The final total amount after tax and discount are applied",
    )
    invoice = models.OneToOneField(
        "Invoice",
        on_delete=models.CASCADE,
        related_name="total",
        verbose_name=_("Invoice"),
        help_text=_("The invoice associated with this total."),
        db_comment="Reference to the associated invoice",
    )

    def save(self, *args, **kwargs):
        InvoiceTotalService().calculate_and_save(self, *args, **kwargs)

    def __str__(self):
        return f"Total for Invoice {self.invoice.pk}"

    def __repr__(self):
        return f"<InvoiceTotal(subtotal={self.subtotal}, total_amount={self.total_amount})>"

    class Meta:
        verbose_name = _("Invoice Total")
        verbose_name_plural = _("Invoice Totals")
        db_table = "sage_invoice_totals"
