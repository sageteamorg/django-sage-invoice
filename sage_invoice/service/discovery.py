import os
from django.apps import apps
from django.conf import settings

class JinjaTemplateDiscovery:
    def __init__(self):
        self.default_template_dir = "default_invoices"  # inside package
        self.sage_template_dir = (
            settings.SAGE_MODEL_TEMPLATE
        )  # custom templates folder name
        self.sage_template_prefix = settings.SAGE_MODEL_PREFIX  # custom template prefix

    def get_default_templates(self, is_receipt=False):
        """Return a list of default templates found in the package's template directory."""
        default_path = os.path.join(
            apps.get_app_config("sage_invoice").path,
            "templates",
            self.default_template_dir,
        )
        return self._find_templates_in_directory(default_path, is_receipt)

    def get_custom_templates(self, is_receipt=False):
        """Return a list of custom templates found in each app's `templates/` directory."""
        template_choices = []
        for app_config in apps.get_app_configs():
            template_dir = os.path.join(
                app_config.path, "templates", self.sage_template_dir
            )
            if os.path.exists(template_dir):
                template_choices.extend(
                    self._find_templates_in_directory(
                        template_dir, is_receipt, self.sage_template_prefix
                    )
                )
        return template_choices

    def _find_templates_in_directory(self, directory, is_receipt=False, prefix=None):
        """
        Helper method to find .jinja2 files in a directory, optionally filtering by
        prefix or `is_receipt`, and return the filenames without the .jinja2 extension.
        """
        if not os.path.exists(directory):
            return []

        templates = []
        for filename in os.listdir(directory):
            if filename.endswith(".jinja2") and (
                not prefix or filename.startswith(prefix)
            ):
                # Filter based on is_receipt
                if is_receipt and "receipt" in filename:
                    templates.append(filename)
                elif not is_receipt and "receipt" not in filename:
                    templates.append(filename)

        # Remove the .jinja2 extension from the filenames
        filenames = list(map(lambda x: x.replace(".jinja2", ""), templates))

        return filenames
