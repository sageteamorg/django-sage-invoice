from django.db import models
from django.utils.translation import gettext_lazy as _


class InvoiceItem(models.Model):
    description = models.CharField(
        max_length=255,
        verbose_name=_("Description"),
        help_text=_("Description of the item."),
        db_comment="Description of the invoice item",
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        help_text=_("The quantity of the item."),
        db_comment="The quantity of the invoice item",
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Unit Price"),
        help_text=_("The price per unit of the item."),
        db_comment="The price per unit of the invoice item",
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Total Price"),
        help_text=_("Auto Genrated total price for this item (quantity * unit price)."),
        db_comment="The total price calculated as quantity * unit price",
    )
    invoice = models.ForeignKey(
        "Invoice",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Invoice"),
        help_text=_("The invoice associated with this item."),
        db_comment="The associated invoice for this item",
    )

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.quantity} x {self.unit_price}"

    def __repr__(self):
        return f"Invoice item> {self.description} - {self.quantity} x {self.unit_price}"

    class Meta:
        verbose_name = _("Invoice Item")
        verbose_name_plural = _("Invoice Items")
        db_table = "sage_invoice_items"
