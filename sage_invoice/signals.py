import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError, OperationalError, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from sage_invoice.service.total import ExpenseService

from .models import Expense, Invoice

logger = logging.getLogger()


@receiver(post_save, sender=Invoice)
def update_invoice_total_on_save(sender, instance, created, **kwargs):
    def recalculate_total():
        invoice_total, _ = Expense.objects.get_or_create(invoice=instance)
        ExpenseService().calculate_and_save(invoice_total)

    try:
        transaction.on_commit(recalculate_total)
    except IntegrityError as e:
        logger.error("Integrity error occurred for invoice %s: %s", instance.title, e)
    except OperationalError as e:
        logger.error(
            "Operational error in database for invoice %s: %s", instance.title, e
        )
    except ValidationError as e:
        logger.error("Validation error for invoice %s: %s", instance.title, e)
    except Exception as e:
        logger.exception(
            "Unexpected error occurred for invoice %s: %s", instance.title, e
        )
