from datetime import datetime
from decimal import Decimal
from unittest import mock

import pytest
from jinja2.exceptions import TemplateNotFound

from sage_invoice.models import Invoice, InvoiceCategory, InvoiceColumn, InvoiceTotal
from sage_invoice.service.discovery import JinjaTemplateDiscovery
from sage_invoice.service.invoice_create import QuotationService
from sage_invoice.service.total import InvoiceTotalService


class TestQuotationService:

    @pytest.fixture
    def template_discovery(self):
        with mock.patch(
            "os.listdir", return_value=["invoice1.jinja2", "invoice2.jinja2"]
        ):
            return JinjaTemplateDiscovery(models_dir="test_templates")

    def test_get_template_path(self, template_discovery):
        template_path = template_discovery.get_template_path("1")
        assert template_path is not None

    def test_render_quotation(self, template_discovery):
        invoice = mock.Mock()
        invoice.template_choice = "invoice1"
        invoice.items.all.return_value = []
        invoice.total.subtotal = 100.00
        invoice.total.tax_percentage = 10.00
        invoice.total.tax_amount = 10.00
        invoice.total.discount_percentage = 5.00
        invoice.total.discount_amount = 5.00
        invoice.total.total_amount = 105.00
        invoice.customer_name = "John Doe"
        invoice.customer_email = "john.doe@example.com"
        invoice.invoice_date = datetime(2024, 8, 25)
        invoice.status = "unpaid"
        invoice.notes = "Test notes"
        invoice.logo.url = "test_logo_url"
        invoice.signature.url = "test_signature_url"
        invoice.stamp.url = "test_stamp_url"

        with mock.patch("jinja2.Environment.get_template") as mock_get_template:
            mock_template = mock.Mock()
            mock_template.render.return_value = "Rendered content"
            mock_get_template.return_value = mock_template

            service = QuotationService()
            service.template_discovery = template_discovery

            queryset = mock.Mock()
            queryset.first.return_value = invoice

            rendered_content = service.render_quotation(queryset)

            mock_get_template.assert_called_once_with("invoice1.jinja2")
            mock_template.render.assert_called_once()
            assert rendered_content == "Rendered content"

    def test_invalid_quotation(self, template_discovery):
        invoice = mock.Mock()
        invoice.template_choice = "NOTFUND"
        invoice.items.all.return_value = []
        invoice.total.subtotal = 100.00
        invoice.total.tax_percentage = 10.00
        invoice.total.tax_amount = 10.00
        invoice.total.discount_percentage = 5.00
        invoice.total.discount_amount = 5.00
        invoice.total.total_amount = 105.00
        invoice.customer_name = "John Doe"
        invoice.customer_email = "john.doe@example.com"
        invoice.invoice_date = datetime(2024, 8, 25)
        invoice.status = "unpaid"
        invoice.notes = "Test notes"
        invoice.logo.url = "test_logo_url"
        invoice.signature.url = "test_signature_url"
        invoice.stamp.url = "test_stamp_url"

        with mock.patch("jinja2.Environment.get_template") as mock_get_template:
            mock_template = mock.Mock()
            mock_template.render.return_value = "Rendered content"
            mock_get_template.return_value = mock_template

            service = QuotationService()
            service.template_discovery = template_discovery

            queryset = mock.Mock()
            queryset.first.return_value = invoice
            with pytest.raises(TemplateNotFound):
                service.render_quotation(queryset)

    def test_render_quotation_with_items(self, template_discovery):
        invoice = mock.Mock()
        invoice.template_choice = "invoice1"

        item1 = mock.Mock(
            description="Item 1", quantity=1, unit_price=100.00, total_price=100.00
        )
        item2 = mock.Mock(
            description="Item 2", quantity=2, unit_price=50.00, total_price=100.00
        )
        invoice.items.all.return_value = [item1, item2]

        mock_query_set = mock.Mock()
        mock_query_set.order_by.return_value = [
            mock.Mock(column_name="Delivery Date", value="2024-09-01"),
            mock.Mock(column_name="Warranty Period", value="12 months"),
        ]
        InvoiceColumn.objects.filter = mock.Mock(return_value=mock_query_set)

        invoice.total.subtotal = 200.00
        invoice.total.tax_percentage = 10.00
        invoice.total.tax_amount = 20.00
        invoice.total.discount_percentage = 5.00
        invoice.total.discount_amount = 10.00
        invoice.total.total_amount = 210.00
        invoice.customer_name = "John Doe"
        invoice.customer_email = "john.doe@example.com"
        invoice.invoice_date = datetime(2024, 8, 25)
        invoice.status = "unpaid"
        invoice.notes = "Test notes"
        invoice.logo.url = "test_logo_url"
        invoice.signature.url = "test_signature_url"
        invoice.stamp.url = "test_stamp_url"

        with mock.patch("jinja2.Environment.get_template") as mock_get_template:
            mock_template = mock.Mock()
            mock_template.render.return_value = "Rendered content"
            mock_get_template.return_value = mock_template

            service = QuotationService()
            service.template_discovery = template_discovery

            queryset = mock.Mock()
            queryset.first.return_value = invoice

            rendered_content = service.render_quotation(queryset)

            mock_get_template.assert_called_once_with("invoice1.jinja2")
            mock_template.render.assert_called_once()

            InvoiceColumn.objects.filter.assert_called()
            assert rendered_content == "Rendered content"


class TestInvoiceTotalService:

    @pytest.fixture
    def invoice_category(self, db):
        """Fixture to create a real InvoiceCategory instance."""
        return InvoiceCategory.objects.create(
            title="Default Category", description="A default category for testing."
        )

    @pytest.fixture
    def invoice(self, db, invoice_category):
        """Fixture to create a real Invoice instance with items."""
        invoice = Invoice.objects.create(
            title="Test Invoice",
            invoice_date="2024-08-25",
            customer_name="John Doe",
            customer_email="john.doe@example.com",
            status="unpaid",
            category=invoice_category,
            due_date="2024-09-01",
        )
        invoice.items.create(
            description="Item 1", quantity=1, unit_price=Decimal("100.00")
        )
        invoice.items.create(
            description="Item 2", quantity=2, unit_price=Decimal("50.00")
        )
        return invoice

    @pytest.fixture
    def invoice_total(self, invoice):
        """Fixture to create an InvoiceTotal instance."""
        return InvoiceTotal.objects.create(
            tax_percentage=Decimal("10.00"),
            discount_percentage=Decimal("5.00"),
            invoice=invoice,
        )

    def test_calculate_and_save(self, invoice_total):
        """Test the calculate_and_save method of InvoiceTotalService."""
        service = InvoiceTotalService()

        with mock.patch.object(InvoiceTotal, "save_base") as mock_save_base:
            service.calculate_and_save(invoice_total)

            assert invoice_total.subtotal == Decimal("200.00")
            assert invoice_total.tax_amount == Decimal("20.00")
            assert invoice_total.discount_amount == Decimal("10.00")
            assert invoice_total.total_amount == Decimal("210.00")
            mock_save_base.assert_called_once()

    def test_calculate_and_save_with_no_items(self, db, invoice_category):
        """Test calculate_and_save when the invoice has no items."""
        invoice = Invoice.objects.create(
            title="Empty Invoice",
            invoice_date="2024-08-25",
            customer_name="John Doe",
            customer_email="john.doe@example.com",
            status="unpaid",
            category=invoice_category,
            due_date="2024-09-01",
        )

        invoice_total = InvoiceTotal.objects.create(
            tax_percentage=Decimal("10.00"),
            discount_percentage=Decimal("5.00"),
            invoice=invoice,
        )

        service = InvoiceTotalService()

        with mock.patch.object(InvoiceTotal, "save_base") as mock_save_base:
            service.calculate_and_save(invoice_total)

            assert invoice_total.subtotal == Decimal("0.00")
            assert invoice_total.tax_amount == Decimal("0.00")
            assert invoice_total.discount_amount == Decimal("0.00")
            assert invoice_total.total_amount == Decimal("0.00")
            mock_save_base.assert_called_once()
