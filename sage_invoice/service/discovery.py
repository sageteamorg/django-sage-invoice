import os

from django.conf import settings


class JinjaTemplateDiscovery:
    SAGE_MODEL_PREFIX = getattr(settings, "SAGE_MODEL_PREFIX", "quotation")
    receipt_prefix = "receipt"

    def __init__(self, models_dir: str = "templates"):
        self.models_dir = os.path.join(
            settings.BASE_DIR, "sage_invoice", "templates", models_dir
        )
        self.SAGE_MODEL_TEMPLATEs = {}
        self.receipt_templates = {}
        self.discover()

    def discover(self):
        """Discovers model and receipt template files in the specified models
        directory and categorizes them into SAGE_MODEL_TEMPLATEs and.

        receipt_templates dictionaries.
        """
        for filename in os.listdir(self.models_dir):
            if filename.endswith(".jinja2"):
                if filename.startswith(self.SAGE_MODEL_PREFIX):
                    name, _ = os.path.splitext(filename)
                    if len(self.SAGE_MODEL_PREFIX) <= len(".jinja2"):
                        template_name = "".join(filter(str.isdigit, name))
                    else:
                        template_name = filename[
                            len(self.SAGE_MODEL_PREFIX) : -len(".jinja2")
                        ]

                    self.SAGE_MODEL_TEMPLATEs[template_name] = os.path.join(
                        self.models_dir, filename
                    )
                elif filename.startswith(self.receipt_prefix):
                    name, _ = os.path.splitext(filename)
                    if len(self.receipt_prefix) <= len(".jinja2"):
                        template_name = "".join(filter(str.isdigit, name))
                    else:
                        template_name = filename[
                            len(self.receipt_prefix) : -len(".jinja2")
                        ]
                    self.receipt_templates[template_name] = os.path.join(
                        self.models_dir, filename
                    )

    def get_template_path(self, template_choice, is_receipt=False):
        """Returns the template path based on the template choice and whether
        it is a receipt.
        """
        if is_receipt:
            return self.receipt_templates.get(template_choice)
        else:
            return self.SAGE_MODEL_TEMPLATEs.get(template_choice)
