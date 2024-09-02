from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.dispatch import receiver

from sage_invoice.service.total import InvoiceTotalService

from .models import Invoice, InvoiceTotal


@receiver(pre_save, sender=Invoice)
def update_invoice_total_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Invoice.objects.get(pk=instance.pk)
        except ObjectDoesNotExist:
            return
        invoice_total, _ = InvoiceTotal.objects.get_or_create(invoice=instance)
        InvoiceTotalService().calculate_and_save(invoice_total)
