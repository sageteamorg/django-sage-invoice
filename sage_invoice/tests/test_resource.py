import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from sage_invoice.models import Invoice, Item, Column, Expense
from sage_invoice.resource import InvoiceResource,Category,ItemResource, ExpenseResource


@pytest.mark.django_db
class TestInvoiceResource:

    @pytest.fixture
    def invoice(self, db):
        return Invoice.objects.create(
            title="Test Invoice",
            invoice_date="2024-09-10",
            customer_name="John Doe",
            status="unpaid",
            tracking_code="INV-20240910",
            due_date="2024-09-20"  # Add the due_date here
        )

    @pytest.fixture
    def invoice_item(self, invoice):
        return Item.objects.create(
            invoice=invoice,
            description="Item 1",
            quantity=2,
            unit_price=Decimal("100.00"),
            total_price=Decimal("200.00"),
        )

    @pytest.fixture
    def invoice_column(self, invoice, invoice_item):
        return Column.objects.create(
            invoice=invoice,
            item=invoice_item,
            column_name="Column 1",
            value="Value 1",
            priority=1,
        )

    @pytest.fixture
    def expense(self, invoice):
        return Expense.objects.create(
            invoice=invoice,
            subtotal=Decimal("1000.00"),
            tax_percentage=Decimal("10.00"),
            tax_amount=Decimal("100.00"),
            discount_percentage=Decimal("5.00"),
            discount_amount=Decimal("50.00"),
            total_amount=Decimal("1050.00"),
        )


    @patch.object(Expense, 'objects')
    def test_create_expenses(self, mock_objects, invoice):
        """Test the create_expenses method."""
        mock_objects.update_or_create = MagicMock()
        resource = InvoiceResource()

        resource.create_expenses("1000.00|10.00|5.00|0", invoice.id)

        mock_objects.update_or_create.assert_called_once_with(
            invoice_id=invoice.id,
            defaults={
                "subtotal": Decimal("1000.00"),
                "tax_percentage": Decimal("10.00"),
                "discount_percentage": Decimal("5.00"),
                "tax_amount": Decimal("100.00"),
                "discount_amount": Decimal("50.00"),
                "total_amount": Decimal("1050.00"),
            }
        )

    def test_dehydrate_items(self, invoice, invoice_item):
        """Test the dehydrate_items method."""
        resource = InvoiceResource()
        result = resource.dehydrate_items(invoice)
        assert result is not None

    def test_dehydrate_columns(self, invoice, invoice_column):
        """Test the dehydrate_columns method."""
        resource = InvoiceResource()
        result = resource.dehydrate_columns(invoice)
        assert result == "Column 1|Value 1|1"

    def test_dehydrate_totals(self, invoice, expense):
        """Test the dehydrate_totals method."""
        resource = InvoiceResource()
        result = resource.dehydrate_totals(invoice)
        assert result == "1000.00|10.00|5.00|0.00"

    def test_dehydrate_contacts(self, invoice):
        """Test the dehydrate_contacts method."""
        invoice.contacts = [{"email": "test@example.com", "phone": "123456789"}]
        invoice.save()

        resource = InvoiceResource()
        result = resource.dehydrate_contacts(invoice)
        assert result == '[{"email": "test@example.com", "phone": "123456789"}]'


@pytest.mark.django_db
class TestItemResource:

    def test_meta(self):
        """Test that ItemResource meta is set correctly."""
        resource = ItemResource()
        assert resource.Meta.model == Item
        assert resource.Meta.fields == ("id", "invoice", "description", "quantity", "unit_price", "total_price")
        assert resource.Meta.import_id_fields == ["id"]


@pytest.mark.django_db
class TestExpenseResource:

    def test_meta(self):
        """Test that ExpenseResource meta is set correctly."""
        resource = ExpenseResource()
        assert resource.Meta.model == Expense
        assert resource.Meta.fields == ("id", "invoice", "subtotal", "tax_percentage", "tax_amount", "discount_percentage", "discount_amount", "total_amount")
        assert resource.Meta.import_id_fields == ["id"]

import pytest
from unittest.mock import patch, MagicMock
from sage_invoice.models import Invoice, Category
from sage_invoice.resource import InvoiceResource

@pytest.mark.django_db
class TestInvoiceResourceWithCategory:

    @pytest.fixture
    def category(self):
        """Fixture to create a category."""
        return Category.objects.create(title="Consulting", description="Consulting Services")

    @pytest.fixture
    def invoice_with_category(self, category):
        """Fixture to create an invoice with a category."""
        return Invoice.objects.create(
            title="Invoice with Category",
            invoice_date="2024-09-11",
            customer_name="Jane Doe",
            status="paid",
            due_date="2024-09-30",
            category=category,
        )

    @pytest.fixture
    def invoice_without_category(self):
        """Fixture to create an invoice without a category."""
        return Invoice.objects.create(
            title="Invoice without Category",
            invoice_date="2024-09-11",
            customer_name="John Doe",
            status="unpaid",
            due_date="2024-09-30"
        )

    def test_dehydrate_category(self, invoice_with_category):
        """Test the dehydrate_category method when a category exists."""
        resource = InvoiceResource()
        result = resource.dehydrate_category(invoice_with_category)
        assert result == "Consulting|Consulting Services"

    def test_dehydrate_category_no_category(self, invoice_without_category):
        """Test the dehydrate_category method when no category is assigned."""
        resource = InvoiceResource()
        result = resource.dehydrate_category(invoice_without_category)
        assert result == ""

    def test_import_category_empty(self, invoice_without_category):
        """Test that an empty category field does not assign a category."""
        resource = InvoiceResource()

        row = {
            "id": invoice_without_category.id,
            "category": ""  # Empty category field
        }

        # Simulate the after_import_row method
        resource.after_import_row(row, None)

        # Ensure that the category is not assigned
        invoice = Invoice.objects.get(id=row["id"])
        assert invoice.category is None
