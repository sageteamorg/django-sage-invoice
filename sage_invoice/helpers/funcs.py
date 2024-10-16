import os
import secrets
from datetime import datetime

from django.conf import settings

from sage_invoice.service.discovery import JinjaTemplateDiscovery


def get_template_choices():
    """
    Returns a combined list of default and custom templates, formatted for use in a
    model's choices field.
    """
    discovery = JinjaTemplateDiscovery()
    default_templates = discovery.get_default_templates()
    custom_templates = discovery.get_custom_templates()

    choices = [(template, template) for template in default_templates]
    choices += [(template, template) for template in custom_templates]

    if not choices:
        return [("", "No templates available")]

    return choices


def generate_tracking_code(user_input: str, creation_date: datetime) -> str:
    """Generate a unique tracking code based on user input and the creation
    date.

    Returns:
        str: A unique tracking code.
    """
    date_str = creation_date.strftime("%Y%m%d")
    random_number = secrets.randbelow(8000) + 1000
    tracking_code = f"{user_input}-{date_str}-{random_number}"
    return tracking_code
