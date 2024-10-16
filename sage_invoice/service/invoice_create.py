import logging
import os
from typing import Any, Dict

from django.conf import settings
from django.db.models import QuerySet
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateNotFound

from sage_invoice.models import Column

from .discovery import JinjaTemplateDiscovery

logger = logging.getLogger(__name__)


class QuotationService:
    """Service class to handle the generation and rendering of quotations."""

    def __init__(self) -> None:
        """Initialize the QuotationService with the template discovery and
        Jinja2.
        """
        logger.info("Initializing QuotationService")
        self.template_discovery = JinjaTemplateDiscovery(
            models_dir=getattr(settings, "SAGE_MODEL_TEMPLATE", "default_invoices")
        )
        self.env = Environment(
            loader=FileSystemLoader(self.template_discovery.models_dir),
            autoescape=select_autoescape(
                ["html", "xml"]
            ),  # Enable autoescape for HTML and XML templates
        )
        logger.info(
            "Template discovery set to directory: %s",
            self.template_discovery.models_dir,
        )

    def render_quotation(self, queryset: QuerySet) -> str:
        """Render the quotation for the given queryset.

        Args:
            queryset (QuerySet): A queryset containing the invoice to render.

        Returns:
            str: The rendered HTML of the quotation.

        Raises:
            TemplateNotFound: If the selected template is not found.
        """
        logger.info("Rendering quotation")
        invoice = queryset.first()
        context = self.render_contax(queryset)
        is_receipt = invoice.receipt
        template_number = "".join(filter(str.isdigit, invoice.template_choice))
        logger.info("Selected template number: %s", template_number)
        selected_template = self.template_discovery.get_template_path(
            template_number, is_receipt
        )
        if not selected_template:
            logger.error("Template %s not found", invoice.template_choice)
            raise TemplateNotFound(f"Template {invoice.template_choice} not found.")
        template = self.env.get_template(os.path.basename(selected_template))
        logger.info("Rendering template: %s", selected_template)

        return template.render(context)

    def render_contax(self, queryset: QuerySet) -> Dict[str, Any]:
        """Prepare the context data for rendering a quotation.

        Args:
            queryset (QuerySet): A queryset containing the invoice(s).

        Returns:
            Dict[str, Any]: The context data for rendering the quotation.
        """
        logger.info("Preparing context data for quotation")
        invoice = queryset
        total = invoice.total
        items = invoice.items.all()
        email = None
        phone = ""
        item_list = []
        custom_columns = set()
        additional_fields = invoice.notes if hasattr(invoice, "notes") else []
        contacts = invoice.contacts

        for contact in contacts:
            if "@" in contact and not email:
                email = contact
            elif contact.isdigit() and not phone:
                phone = contact

        for item in items:
            custom_data = Column.objects.filter(item=item).order_by("priority")
            custom_fields = {data.column_name: data.value for data in custom_data}
            custom_columns.update(custom_fields.keys())
            item_dict = {
                "description": item.description,
                "quantity": item.quantity,
                "measurement": item.measurement if item.measurement else "",
                "unit_price": item.unit_price,
                "total_price": item.total_price,
                "custom_data": custom_fields,
            }
            item_list.append(item_dict)

        context = {
            "title": invoice.title,
            "tracking_code": invoice.tracking_code,
            "items": item_list,
            "subtotal": total.subtotal,
            "tax_percentage": total.tax_percentage,
            "tax_amount": total.tax_amount,
            "discount_percentage": total.discount_percentage,
            "discount_amount": total.discount_amount,
            "concession_percentage": total.concession_percentage,
            "concession_amount": total.concession_amount,
            "grand_total": total.total_amount,
            "invoice_date": invoice.invoice_date,
            "customer_name": invoice.customer_name,
            "customer_email": email,
            "customer_phone": phone,
            "due_date": invoice.due_date,
            "status": invoice.status,
            "currency": invoice.currency,
            "logo_url": invoice.logo.url if invoice.logo else None,
            "sign_url": invoice.signature.url if invoice.signature else None,
            "stamp_url": invoice.stamp.url if invoice.stamp else None,
            "custom_columns": custom_columns,
            "additional_fields": additional_fields,
        }

        logger.info("Context prepared for invoice: %s", invoice.title)
        return context
