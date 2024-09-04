from django.apps import AppConfig


class InvoiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sage_invoice"

    def ready(self) -> None:
        import sage_invoice.check
        import sage_invoice.signals
