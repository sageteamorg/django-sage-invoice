import os

from django.conf import settings


class JinjaTemplateDiscovery:
    model_prefix = getattr(settings, "MODEL_PREFIX", "quotation")

    def __init__(self, models_dir: str = "templates"):
        self.models_dir = os.path.join(
            settings.BASE_DIR, "sage_invoice", "templates", models_dir
        )
        self.model_templates = {}
        self.discover()

    def discover(self):
        """
        Discovers model and enum template files in the specified models directory and categorizes them
        into model and enum templates dictionaries.
        """
        for filename in os.listdir(self.models_dir):
            if filename.endswith(".jinja2"):
                if filename.startswith(self.model_prefix):
                    template_name = filename[len(self.model_prefix) : -len(".jinja2")]
                    self.model_templates[template_name] = os.path.join(
                        self.models_dir, filename
                    )

    def get_template_path(self, template_choice):
        """
        Returns the template path based on the template choice.
        """
        return self.model_templates.get(template_choice)
