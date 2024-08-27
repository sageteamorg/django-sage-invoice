import os

from django.conf import settings
from django.db import models

from sage_invoice.service.discovery import JinjaTemplateDiscovery


class InvoiceStatus(models.TextChoices):
    PAID = ("paid", "PAID")
    UNPAID = ("unpaid", "UNPAID")


def get_template_choices():
    """
    Dynamically generates the template choices based on the templates discovered by JinjaTemplateDiscovery.
    Only the base name of the template is shown in the choices.
    """
    template_discovery = JinjaTemplateDiscovery(
        models_dir=getattr(settings, "MODEL_TEMPLATE", "sage_invoice")
    )
    choices = [
        (
            key,
            f"{os.path.basename(value).replace('.jinja2', '').replace('_', ' ').title()} Template",
        )
        for key, value in template_discovery.model_templates.items()
    ]
    return choices or [("", "No Templates Available")]
