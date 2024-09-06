import os

from django.conf import settings

from sage_invoice.service.discovery import JinjaTemplateDiscovery


def get_template_choices(is_receipt=False):
    """Dynamically generates the template choices based on the templates Only
    the base name of the template is shown in the choices.
    """
    template_discovery = JinjaTemplateDiscovery(
        models_dir=getattr(settings, "SAGE_MODEL_TEMPLATE", "sage_invoice")
    )

    templates = (
        template_discovery.receipt_templates
        if is_receipt
        else template_discovery.SAGE_MODEL_TEMPLATEs
    )

    choices = [
        (
            key,
            f"{os.path.basename(value).replace('.jinja2', '').replace('_', ' ').title()} Template",
        )
        for key, value in templates.items()
    ]

    return choices or [("", "No Templates Available")]
