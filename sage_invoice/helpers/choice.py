from django.db import models


class InvoiceStatus(models.TextChoices):
    PAID = ("paid", "PAID")
    UNPAID = ("unpaid", "UNPAID")
