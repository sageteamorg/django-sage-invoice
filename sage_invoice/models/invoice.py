from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_tools.mixins.models import TitleSlugMixin

from sage_invoice.helpers.choice import InvoiceStatus, get_template_choices


class Invoice(TitleSlugMixin):
    invoice_date = models.DateField(
        verbose_name=_("Invoice Date"),
        help_text=_("The date when the invoice was created."),
        db_comment="Invoice date created",
    )
    customer_name = models.CharField(
        max_length=255,
        verbose_name=_("Customer Name"),
        help_text=_("The name of the customer."),
        db_comment="Customer name created",
    )
    tracking_code = models.CharField(
        max_length=255,
        verbose_name=_("Tracking Code"),
        help_text=_("The tracking code of the invoice."),
        db_comment="Tracking code created",
    )
    customer_email = models.EmailField(
        verbose_name=_("Customer Email"),
        help_text=_("The email of the customer."),
        db_comment="Customer email created",
    )
    status = models.CharField(
        max_length=50,
        choices=InvoiceStatus,
        verbose_name=_("Status"),
        help_text=_("The current status of the invoice (Paid, Unpaid)."),
        db_comment="Current status of the invoice (Paid, Unpaid)",
    )
    receipt = models.BooleanField(
        verbose_name=_("Receipt"),
        default=False,
        help_text=_("Is this a receipt or an invoice"),
        db_comment="Check if this invoice is a receipt",
    )
    notes = models.TextField(
        verbose_name=_("Notes"),
        blank=True,
        null=True,
        help_text=_("Additional notes regarding the invoice."),
        db_comment="Additional notes regarding the invoice",
    )
    category = models.ForeignKey(
        "InvoiceCategory",
        on_delete=models.CASCADE,
        related_name="category",
        null=False,
        blank=False,
        verbose_name=_("Category"),
        help_text=_("The category associated with this invoice."),
        db_comment="Category associated with this invoice",
    )
    due_date = models.DateField(
        verbose_name=_("Due Date"),
        help_text=_("The date by which the invoice should be paid."),
        db_comment="Due date of the invoice",
    )
    logo = models.ImageField(
        upload_to="invoices/logos/",
        blank=True,
        null=True,
        verbose_name=_("Logo"),
        help_text=_("The logo displayed on the invoice."),
        db_comment="Logo displayed on the invoice",
    )
    signature = models.ImageField(
        upload_to="invoices/signatures/",
        blank=True,
        null=True,
        verbose_name=_("Signature"),
        help_text=_("The signature image for the invoice."),
        db_comment="Signature image for the invoice",
    )
    stamp = models.ImageField(
        upload_to="invoices/stamps/",
        blank=True,
        null=True,
        verbose_name=_("Stamp"),
        help_text=_("The stamp image for the invoice."),
        db_comment="Stamp image for the invoice",
    )
    template_choice = models.CharField(
        verbose_name=_("Template choice"),
        max_length=20,
        choices=get_template_choices(),
        help_text=_("The template you want for your invoice"),
        db_comment="Template choice for the invoice",
    )

    def clean(self):
        if self.due_date <= self.invoice_date:
            raise ValidationError(_("Due Date must be later than Invoice Date."))

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
        db_table = "sage_invoice"

    def __str__(self):
        return f"Invoice {self.pk} - {self.customer_name}"

    def __repr__(self):
        return f"<Invoice {self.pk}>"
