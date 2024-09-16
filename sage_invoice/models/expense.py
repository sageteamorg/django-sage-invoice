from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class Expense(models.Model):
    subtotal = models.DecimalField(
        verbose_name=_("Subtotal"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("The sum of all item totals."),
        db_comment="Sum of all item totals in the invoice",
    )
    tax_percentage = models.DecimalField(
        verbose_name=_("Tax Percentage"),
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("The tax percentage applied to the invoice."),
        db_comment="The percentage of tax applied to the invoice",
    )
    discount_percentage = models.DecimalField(
        verbose_name=_("Discount Percentage"),
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("The discount percentage applied to the invoice."),
        db_comment="The percentage of discount applied to the invoice",
    )
    concession_percentage = models.DecimalField(
        verbose_name=_("Concession Percentage"),
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("The concession percentage applied to the invoice."),
        db_comment="The percentage of concession applied to the invoice",
    )
    tax_amount = models.DecimalField(
        verbose_name=_("Tax Amount"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("The calculated tax amount."),
        db_comment="The total tax amount calculated based on the subtotal and tax percentage",
    )
    discount_amount = models.DecimalField(
        verbose_name=_("Discount Amount"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("The calculated discount amount."),
        db_comment="The total discount amount calculated based on the subtotal and discount percentage",
    )
    concession_amount = models.DecimalField(
        verbose_name=_("Concession Amount"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("The calculated concession amount."),
        db_comment="The total concession amount calculated based on the subtotal and discount percentage",
    )
    total_amount = models.DecimalField(
        verbose_name=_("Total Amount"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("The final total after applying tax and discount."),
        db_comment="The final total amount after tax and discount are applied",
    )
    invoice = models.OneToOneField(
        "Invoice",
        verbose_name=_("Invoice"),
        on_delete=models.CASCADE,
        related_name="total",
        help_text=_("The invoice associated with this total."),
        db_comment="Reference to the associated invoice",
    )

    def __str__(self):
        return f"Expense {self.invoice.pk}"

    def __repr__(self):
        return f"<Expense(subtotal={self.subtotal}, total_amount={self.total_amount})>"

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")
        db_table = "sage_expense"
