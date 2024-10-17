import pytest
from unittest.mock import patch, MagicMock
from jinja2.exceptions import TemplateNotFound
from sage_invoice.service.invoice_create import QuotationService
from sage_invoice.models import Invoice, Item, Expense
from sage_invoice.service.total import ExpenseService
from unittest import mock
from decimal import Decimal
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestQuotationService:

    @patch('sage_invoice.service.invoice_create.JinjaTemplateDiscovery')
    def test_init(self, mock_template_discovery):
        # Test if QuotationService initializes correctly
        service = QuotationService()
        assert service.template_discovery == mock_template_discovery.return_value
        assert service.env is not None
        mock_template_discovery.assert_called_once_with(
            sage_template_dir="sage_invoice"  # Default directory
        )

    @pytest.fixture
    def invoice(self, db):
        # Create a sample invoice and related items
        invoice = Invoice.objects.create(
            title="Test Invoice",
            invoice_date="2024-09-10",
            customer_name="Test Customer",
            tracking_code="INV-2024",
            status="unpaid",
            currency="USD",
            due_date="2024-10-10"
        )
        Expense.objects.create(
            invoice=invoice,
            subtotal=100,
            tax_percentage=10,
            discount_percentage=5,
            concession_percentage=0,
            tax_amount=10,
            discount_amount=5,
            concession_amount=0,
            total_amount=105
        )
        Item.objects.create(
            invoice=invoice,
            description="Test Item",
            quantity=1,
            unit_price=100,
            total_price=100
        )
        return invoice

    @patch('sage_invoice.service.invoice_create.JinjaTemplateDiscovery.get_template_path')
    def test_render_quotation_success(self, mock_get_template_path, invoice):
        # Mock template discovery and rendering process
        mock_template = MagicMock()
        mock_template.render.return_value = "Rendered HTML"
        mock_get_template_path.return_value = "path/to/template.html"

        service = QuotationService()
        service.env.get_template = MagicMock(return_value=mock_template)

        # Mock the queryset with first method
        mock_queryset = MagicMock()
        mock_queryset.first.return_value = invoice

        result = service.render_quotation(mock_queryset)

        assert result == "Rendered HTML"
        mock_get_template_path.assert_called_once()
        service.env.get_template.assert_called_once_with("template.html")
        mock_template.render.assert_called_once()

    @patch('sage_invoice.service.invoice_create.JinjaTemplateDiscovery.get_template_path')
    def test_render_quotation_template_not_found(self, mock_get_template_path, invoice):
        # Test case when template is not found
        mock_get_template_path.return_value = None
        service = QuotationService()

        # Mock the queryset with first method
        mock_queryset = MagicMock()
        mock_queryset.first.return_value = invoice

        with pytest.raises(TemplateNotFound):
            service.render_quotation(mock_queryset)

        mock_get_template_path.assert_called_once()

    def test_render_context(self, invoice):
        # Test context generation for the invoice
        service = QuotationService()

        # Ensure contacts and other fields are handled correctly
        invoice.contacts = ["you@example.com", "1234567890"]
        context = service.render_context(invoice)

        assert context["title"] == invoice.title
        assert context["tracking_code"] == invoice.tracking_code
        assert context["subtotal"] == invoice.total.subtotal
        assert context["grand_total"] == invoice.total.total_amount
        assert context["customer_name"] == invoice.customer_name
        assert len(context["items"]) == invoice.items.count()

    def test_invalid_invoice_due_date(self):
        # Test validation on due date
        invoice = Invoice(
            title="Invalid Invoice",
            invoice_date="2024-09-10",
            due_date="2024-09-05",
            customer_name="Test Customer",
            tracking_code="INV-2024",
            status="unpaid",
            currency="USD"
        )
        with pytest.raises(ValidationError):
            invoice.clean()

@pytest.mark.django_db
class TestExpenseService:

    @pytest.fixture
    def invoice(self, db):
        """Fixture to create a real Invoice instance with items."""
        invoice = Invoice.objects.create(
            title="Test Invoice",
            invoice_date="2024-08-25",
            customer_name="John Doe",
            status="unpaid",
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
        """Fixture to create an Expense instance."""
        return Expense.objects.create(
            tax_percentage=Decimal("10.00"),
            discount_percentage=Decimal("5.00"),
            invoice=invoice,
        )

    def test_calculate_and_save(self, invoice_total):
        """Test the calculate_and_save method of ExpenseService."""
        service = ExpenseService()

        with mock.patch.object(Expense, "save") as mock_save:
            service.calculate_and_save(invoice_total)

            # Verify calculations
            assert invoice_total.subtotal == Decimal("200.00")
            assert invoice_total.tax_amount == Decimal("20.00")
            assert invoice_total.discount_amount == Decimal("10.00")
            assert invoice_total.total_amount == Decimal("210.00")
            mock_save.assert_called_once()

    def test_calculate_and_save_with_no_items(self, db):
        """Test calculate_and_save when the invoice has no items."""
        invoice = Invoice.objects.create(
            title="Empty Invoice",
            invoice_date="2024-08-25",
            customer_name="John Doe",
            status="unpaid",
            due_date="2024-09-01",
        )

        invoice_total = Expense.objects.create(
            tax_percentage=Decimal("10.00"),
            discount_percentage=Decimal("5.00"),
            invoice=invoice,
        )

        service = ExpenseService()

        with mock.patch.object(invoice_total, "save") as mock_save:
            service.calculate_and_save(invoice_total)

            # Verify calculations with no items
            assert invoice_total.subtotal == Decimal("0.00")
            assert invoice_total.tax_amount == Decimal("0.00")
            assert invoice_total.discount_amount == Decimal("0.00")
            assert invoice_total.total_amount == Decimal("0.00")
            mock_save.assert_called_once()
