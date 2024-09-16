import pytest
from unittest import mock
from django.db import IntegrityError, OperationalError, transaction
from sage_invoice.models import Invoice, Expense
from sage_invoice.service.total import ExpenseService
from sage_invoice.signals import update_invoice_total_on_save
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestInvoiceSignals:

    @pytest.fixture
    def invoice(self, db):
        """Fixture to create a real Invoice instance."""
        return Invoice.objects.create(
            title="Test Invoice",
            invoice_date="2024-09-01",
            customer_name="John Doe",
            status="unpaid",
            due_date="2024-09-15",
        )

    @mock.patch.object(ExpenseService, "calculate_and_save")
    @mock.patch("sage_invoice.signals.transaction.on_commit")
    def test_update_invoice_total_on_save_success(self, mock_on_commit, mock_calculate_and_save, invoice):
        """Test that the signal correctly calculates and saves the invoice total."""
        Expense.objects.create(invoice=invoice, subtotal=100, total_amount=100)

        # Trigger the signal
        update_invoice_total_on_save(Invoice, invoice, created=False)

        # Verify that the recalculate_total function is registered with on_commit
        mock_on_commit.assert_called_once()

        # Call the recalculate_total function manually
        recalculate_total_fn = mock_on_commit.call_args[0][0]
        recalculate_total_fn()  # Simulate transaction commit

        mock_calculate_and_save.assert_called_once()

    @mock.patch.object(ExpenseService, "calculate_and_save")
    @mock.patch("sage_invoice.signals.transaction.on_commit")
    def test_update_invoice_total_on_save_transaction_error(self, mock_on_commit, mock_calculate_and_save, invoice):
        """Test that transaction errors are handled correctly."""
        mock_on_commit.side_effect = OperationalError("Transaction failed")

        # Trigger the signal
        update_invoice_total_on_save(Invoice, invoice, created=False)

        mock_calculate_and_save.assert_not_called()

    @mock.patch.object(ExpenseService, "calculate_and_save")
    @mock.patch("sage_invoice.signals.transaction.on_commit")
    def test_update_invoice_total_on_save_integrity_error(self, mock_on_commit, mock_calculate_and_save, invoice):
        """Test that integrity errors are handled correctly."""
        mock_on_commit.side_effect = IntegrityError("Integrity failed")

        # Trigger the signal
        update_invoice_total_on_save(Invoice, invoice, created=False)

        mock_calculate_and_save.assert_not_called()

    @mock.patch.object(ExpenseService, "calculate_and_save")
    @mock.patch("sage_invoice.signals.transaction.on_commit")
    def test_update_invoice_total_on_save_validation_error(self, mock_on_commit, mock_calculate_and_save, invoice):
        """Test that validation errors are handled correctly."""
        mock_on_commit.side_effect = ValidationError("Validation failed")

        # Trigger the signal
        update_invoice_total_on_save(Invoice, invoice, created=False)

        mock_calculate_and_save.assert_not_called()
