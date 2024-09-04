from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InvoiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sage_invoice"
    verbose_name = _("Invoice Management")

    def ready(self) -> None:
        import sage_invoice.check
        import sage_invoice.signals
