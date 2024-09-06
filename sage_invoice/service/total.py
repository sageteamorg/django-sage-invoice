from decimal import Decimal


class ExpenseService:
    """Service class to handle calculations and saving for Expense."""

    def calculate_and_save(self, invoice_total, *args, **kwargs):
        """Calculate the subtotal, tax amount, discount amount, and total
        amount, and then save the instance.
        """
        # Calculate subtotal from related items, ensure it's not None
        invoice_total.subtotal = sum(
            item.total_price for item in invoice_total.invoice.items.all()
        )

        # Convert tax and discount percentages to Decimal
        tax_percentage = Decimal(invoice_total.tax_percentage)
        discount_percentage = Decimal(invoice_total.discount_percentage)

        # Calculate tax amount
        invoice_total.tax_amount = invoice_total.subtotal * (
            tax_percentage / Decimal(100)
        )

        # Calculate discount amount
        invoice_total.discount_amount = invoice_total.subtotal * (
            discount_percentage / Decimal(100)
        )

        # Calculate total amount
        invoice_total.total_amount = (
            invoice_total.subtotal
            + invoice_total.tax_amount
            - invoice_total.discount_amount
        )

        # Save the Expense instance using the standard save method
        invoice_total.save(*args, **kwargs)
