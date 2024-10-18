from django.db import models
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField

class CustomerProfile(models.Model):
    """
    This model stores complete customer information, including contact details,
    billing address, and additional fields required for invoicing.
    """
    invoice = models.OneToOneField(
        "Invoice",
        on_delete=models.CASCADE,
        related_name="customer",
        verbose_name=_("Customer Profile"),
        help_text=_("The customer profile linked to this invoice."),
        db_comment="Link to the customer profile associated with this invoice",
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_("Customer Name"),
        help_text=_("The name of the customer."),
        db_comment="Customer name created",
    )

    company_name = models.CharField(
        max_length=255,
        verbose_name=_("Company Name"),
        blank=True,
        null=True,
        help_text=_("The company name of the customer (optional)."),
        db_comment="Company name associated with the customer, if applicable.",
    )

    billing_address = JSONField(
        verbose_name=_("Billing Address"),
        blank=True,
        null=True,
        schema={
            "type": "object",
            "title": "Billing Address",
            "properties": {
                "street": {"type": "string", "title": "Street", "placeholder": "123 Main St"},
                "city": {"type": "string", "title": "City", "placeholder": "New York"},
                "state": {"type": "string", "title": "State", "placeholder": "NY"},
                "postal_code": {"type": "string", "pattern": "^[0-9]+$", "title": "Postal Code", "placeholder": "10001"},
                "country": {"type": "string", "title": "Country", "placeholder": "USA"},
            },
        },
        help_text=_("The full billing address of the customer."),
        db_comment="Stores billing address details such as street, city, state, postal code, and country.",
    )

    # Optional shipping address (if different from billing)
    shipping_address = JSONField(
        verbose_name=_("Shipping Address"),
        blank=True,
        null=True,
        schema={
            "type": "object",
            "title": "Shipping Address",
            "properties": {
                "street": {"type": "string", "title": "Street", "placeholder": "456 Shipping Ave"},
                "city": {"type": "string", "title": "City", "placeholder": "Los Angeles"},
                "state": {"type": "string", "title": "State", "placeholder": "CA"},
                "postal_code": {"type": "string", "pattern": "^[0-9]+$", "title": "Postal Code", "placeholder": "90001"},
                "country": {"type": "string", "title": "Country", "placeholder": "USA"},
            },
        },
        help_text=_("The shipping address of the customer (optional)."),
        db_comment="Stores shipping address details if different from the billing address.",
    )

    contact = JSONField(
        verbose_name="Customer Contacts",
        blank=True,
        null=True,
        schema={
            "type": "object",
            "properties": {
                "Contact Info": {
                    "oneOf": [
                        {
                            "type": "object",
                            "title": "Phone",
                            "properties": {
                                "phone": {
                                    "type": "string",
                                    "pattern": "^[0-9]+$",
                                    "title": "Phone",
                                    "placeholder": "1234567890",
                                }
                            },
                        },
                        {
                            "type": "object",
                            "title": "Email",
                            "properties": {
                                "email": {
                                    "type": "string",
                                    "format": "email",
                                    "title": "Email",
                                    "placeholder": "you@example.com",
                                }
                            },
                        },
                    ]
                }
            },
        },
    )

    def __str__(self):
        return f"{self.customer_name} ({self.company_name})" if self.company_name else self.customer_name

    class Meta:
        verbose_name = _("Customer Profile")
        verbose_name_plural = _("Customer Profiles")
        db_table = "sage_invoice_customer"
