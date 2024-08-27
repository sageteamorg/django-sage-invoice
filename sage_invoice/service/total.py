class InvoiceTotalService:
    """
    Service class to handle calculations and saving for InvoiceTotal.
    """

    def calculate_and_save(self, invoice_total: dict, *args, **kwargs):
        """
        Calculate the subtotal, tax amount, discount amount, and total amount
        and then save the instance.
        """
        invoice_total.subtotal = sum(
            item.total_price for item in invoice_total.invoice.items.all()
        )

        invoice_total.tax_amount = invoice_total.subtotal * (
            invoice_total.tax_percentage / 100
        )
        invoice_total.discount_amount = invoice_total.subtotal * (
            invoice_total.discount_percentage / 100
        )

        invoice_total.total_amount = (
            invoice_total.subtotal
            + invoice_total.tax_amount
            - invoice_total.discount_amount
        )

        invoice_total.save_base(*args, **kwargs)
