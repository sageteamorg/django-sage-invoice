import logging
import os
import random
from datetime import datetime
from typing import Any, Dict

from django.conf import settings
from django.db.models import QuerySet
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from sage_invoice.models import InvoiceColumn

from .discovery import JinjaTemplateDiscovery

logger = logging.getLogger(__name__)


class QuotationService:
    """
    Service class to handle the generation and rendering of quotations.
    """

    def __init__(self) -> None:
        """
        Initialize the QuotationService with the template discovery and Jinja2
        """
        logger.info("Initializing QuotationService")
        self.template_discovery = JinjaTemplateDiscovery(
            models_dir=getattr(settings, "MODEL_TEMPLATE", "sage_invoice")
        )
        self.env = Environment(
            loader=FileSystemLoader(self.template_discovery.models_dir)
        )
        logger.info(
            "Template discovery set to directory: %s",
            self.template_discovery.models_dir,
        )

    def generate_tracking_code(self, user_input: str, creation_date: datetime) -> str:
        """
        Generate a unique tracking code based on user input
        and the creation date.

        Returns:
            str: A unique tracking code.
        """
        date_str = creation_date.strftime("%Y%m%d")
        random_number = random.randint(1000, 9999)
        tracking_code = f"{user_input}-{date_str}-{random_number}"
        logger.info("Generated tracking code: %s", tracking_code)
        return tracking_code

    def render_quotation(self, queryset: QuerySet) -> str:
        """
        Render the quotation for the given queryset.

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
        template_number = "".join(filter(str.isdigit, invoice.template_choice))
        logger.info("Selected template number: %s", template_number)
        selected_template = self.template_discovery.get_template_path(template_number)
        if not selected_template:
            logger.error("Template %s not found", invoice.template_choice)
            raise TemplateNotFound(f"Template {invoice.template_choice} not found.")
        template = self.env.get_template(os.path.basename(selected_template))
        logger.info("Rendering template: %s", selected_template)

        return template.render(context)

    def render_contax(self, queryset: QuerySet) -> Dict[str, Any]:
        """
        Prepare the context data for rendering a quotation.

        Args:
            queryset (QuerySet): A queryset containing the invoice(s).

        Returns:
            Dict[str, Any]: The context data for rendering the quotation.
        """
        logger.info("Preparing context data for quotation")
        invoice = queryset.first()
        total = invoice.total
        items = invoice.items.all()

        item_list = []
        custom_columns = set()

        for item in items:
            custom_data = InvoiceColumn.objects.filter(item=item).order_by("priority")
            custom_fields = {data.column_name: data.value for data in custom_data}
            custom_columns.update(custom_fields.keys())
            item_dict = {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
                "custom_data": custom_fields,
            }
            item_list.append(item_dict)

        context = {
            "title": invoice.title,
            "tracking_code": self.generate_tracking_code(
                invoice.tracking_code, invoice.invoice_date
            ),
            "items": item_list,
            "subtotal": total.subtotal,
            "tax_percentage": total.tax_percentage,
            "tax_amount": total.tax_amount,
            "discount_percentage": total.discount_percentage,
            "discount_amount": total.discount_amount,
            "grand_total": total.total_amount,
            "invoice_date": invoice.invoice_date,
            "customer_name": invoice.customer_name,
            "customer_email": invoice.customer_email,
            "status": invoice.status,
            "notes": invoice.notes,
            "logo_url": invoice.logo.url if invoice.logo else None,
            "sign_url": invoice.signature.url if invoice.signature else None,
            "stamp_url": invoice.stamp.url if invoice.stamp else None,
            "custom_columns": custom_columns,
        }

        logger.info("Context prepared for invoice: %s", invoice.title)
        return context
