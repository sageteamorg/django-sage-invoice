import os

from django.apps import apps
from django.conf import settings


class JinjaTemplateDiscovery:
    def __init__(self):
        self.default_template_dir = "default_invoices"  # inside package
        self.custom_template_dir = (
            settings.SAGE_MODEL_TEMPLATE
        )  # custom templates folder name
        self.custom_template_prefix = (
            settings.SAGE_MODEL_PREFIX
        )  # custom template prefix

    def get_default_templates(self):
        """Return a list of default templates found in the package's template directory."""
        # Use Django's template loading mechanisms to discover default templates.
        default_path = os.path.join(
            apps.get_app_config("sage_invoice").path,
            "templates",
            self.default_template_dir,
        )
        return self._find_templates_in_directory(default_path)

    def get_custom_templates(self):
        """Return a list of custom templates found in each app's `templates/` directory."""
        template_choices = []
        for app_config in apps.get_app_configs():
            template_dir = os.path.join(
                app_config.path, "templates", self.custom_template_dir
            )
            if os.path.exists(template_dir):
                template_choices.extend(
                    self._find_templates_in_directory(
                        template_dir, self.custom_template_prefix
                    )
                )
        return template_choices

    def _find_templates_in_directory(self, directory, prefix=None):
        """
        Helper method to find .jinja2 files in a directory, optionally filtering by
        prefix.
        """
        if not os.path.exists(directory):
            return []

        templates = []
        for filename in os.listdir(directory):
            if filename.endswith(".jinja2") and (
                not prefix or filename.startswith(prefix)
            ):
                templates.append(filename)
        return templates
