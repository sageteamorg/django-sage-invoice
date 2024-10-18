from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField
from sage_tools.mixins.models import TitleSlugMixin

from sage_invoice.helpers.choice import Currency, InvoiceStatus
from sage_invoice.helpers.funcs import generate_tracking_code, get_template_choices


class Invoice(TitleSlugMixin):
    invoice_date = models.DateField(
        verbose_name=_("Invoice Date"),
        help_text=_("The date when the invoice was created."),
        db_comment="Invoice date created",
    )
    tracking_code = models.CharField(
        max_length=255,
        verbose_name=_("Tracking Code"),
        help_text=_(
            "Enter the first 3-4 characters of the tracking code. The full code will be auto-generated as <prefix> + <date> + <random number>."
        ),
        db_comment="Tracking code created",
    )
    
    status = models.CharField(
        max_length=50,
        choices=InvoiceStatus.choices,
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
    notes = JSONField(
        verbose_name=_("Notes"),
        blank=True,
        null=True,
        help_text=(
            """
            You can add any number of custom fields dynamically,
            such as'Terms & Conditions', 'Technology Tips', etc.
            """
        ),
        db_comment=("This field stores additional dynamic content in JSON format. "),
        schema={
            "type": "array",
            "title": "Additional Fields",
            "items": {
                "type": "object",
                "title": "Field",
                "properties": {
                    "label": {"type": "string", "title": "Field Name"},
                    "content": {
                        "type": "string",
                        "title": "Field Content",
                        "widget": "textarea",
                    },
                },
            },
        },
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="invoices",
        null=True,
        blank=True,
        verbose_name=_("Category"),
        help_text=_("The category associated with this invoice."),
        db_comment="Category associated with this invoice",
    )
    currency = models.CharField(
        max_length=10,
        verbose_name="Currency",
        choices=Currency.choices,
        default=Currency.USD,
        help_text=_("Currency of unit price"),
        db_comment="Which currency is this item ",
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
        # Ensure both `due_date` and `invoice_date` are set before comparing them
        if self.due_date and self.invoice_date:
            if self.due_date < self.invoice_date:
                raise ValidationError(_("Due Date must be later than Invoice Date."))
        else:
            raise ValidationError(_("Both Due Date and Invoice Date must be provided."))

        # Ensure tracking code length is valid
        if self.tracking_code and len(self.tracking_code) <= 10:
            self.tracking_code = generate_tracking_code(
                self.tracking_code, self.invoice_date
            )

    def get_absolute_url(self):
        return reverse("invoice_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
        permissions = [
            ("mark_as_paid", _("Grants mark invoices as paid")),
            ("mark_as_unpaid", _("Grants Can mark invoices as unpaid")),
            ("apply_discount", _("Grants apply discounts to invoices")),
            ("reject_invoice", _("Grants reject invoices")),
        ]
        db_table = "sage_invoice"

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"Invoice> {self.title}>"
