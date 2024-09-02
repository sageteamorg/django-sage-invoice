from import_export import fields, resources
from import_export.widgets import BooleanWidget, DateWidget, ForeignKeyWidget

from sage_invoice.models import (
    Invoice,
    InvoiceCategory,
    InvoiceColumn,
    InvoiceItem,
    InvoiceTotal,
)


class InvoiceItemResource(resources.ModelResource):
    invoice = fields.Field(
        column_name="invoice",
        attribute="invoice",
        widget=ForeignKeyWidget(Invoice, "id"),
    )

    class Meta:
        model = InvoiceItem
        fields = (
            "id",
            "invoice",
            "description",
            "quantity",
            "unit_price",
            "total_price",
        )
        import_id_fields = ["id"]
        skip_unchanged = True
        report_skipped = True


class InvoiceColumnResource(resources.ModelResource):
    invoice = fields.Field(
        column_name="invoice",
        attribute="invoice",
        widget=ForeignKeyWidget(Invoice, "id"),
    )

    class Meta:
        model = InvoiceColumn
        fields = ("id", "invoice", "header", "value")
        import_id_fields = ["id"]
        skip_unchanged = True
        report_skipped = True


class InvoiceTotalResource(resources.ModelResource):
    invoice = fields.Field(
        column_name="invoice",
        attribute="invoice",
        widget=ForeignKeyWidget(Invoice, "id"),
    )

    class Meta:
        model = InvoiceTotal
        fields = (
            "id",
            "invoice",
            "subtotal",
            "tax_percentage",
            "tax_amount",
            "discount_percentage",
            "discount_amount",
            "total_amount",
        )
        import_id_fields = ["id"]
        skip_unchanged = True
        report_skipped = True


class InvoiceResource(resources.ModelResource):
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(InvoiceCategory, "name"),
    )

    invoice_date = fields.Field(
        column_name="invoice_date",
        attribute="invoice_date",
        widget=DateWidget(format="%Y-%m-%d"),
    )

    due_date = fields.Field(
        column_name="due_date",
        attribute="due_date",
        widget=DateWidget(format="%Y-%m-%d"),
    )

    receipt = fields.Field(
        column_name="receipt", attribute="receipt", widget=BooleanWidget()
    )

    # Define custom fields for related objects
    items = fields.Field()
    columns = fields.Field()
    totals = fields.Field()

    class Meta:
        model = Invoice
        fields = (
            "id",
            "title",
            "invoice_date",
            "customer_name",
            "customer_email",
            "status",
            "receipt",
            "category",
            "due_date",
            "tracking_code",
            "notes",
            "logo",
            "signature",
            "stamp",
            "template_choice",
            "items",
            "columns",
            "totals",
        )
        export_order = (
            "id",
            "title",
            "invoice_date",
            "customer_name",
            "customer_email",
            "status",
            "receipt",
            "category",
            "due_date",
            "tracking_code",
            "notes",
            "logo",
            "signature",
            "stamp",
            "template_choice",
            "items",
            "columns",
            "totals",
        )
        import_id_fields = ["id"]
        skip_unchanged = True
        report_skipped = True

    def dehydrate_category(self, invoice):
        category = invoice.category
        if category:
            return category.title
        return ""

    def dehydrate_items(self, invoice):
        items = InvoiceItem.objects.filter(invoice=invoice)
        return "; ".join(
            [
                f"{item.description} (Quantity: {item.quantity}, Unit Price: {item.unit_price}, Total: {item.total_price})"
                for item in items
            ]
        )

    def dehydrate_columns(self, invoice):
        columns = InvoiceColumn.objects.filter(invoice=invoice)
        return "; ".join(
            [f"{column.column_name}: {column.value}" for column in columns]
        )

    def dehydrate_totals(self, invoice):
        totals = InvoiceTotal.objects.filter(invoice=invoice)
        return "; ".join(
            [
                f"Subtotal: {total.subtotal}, Tax: {total.tax_amount} ({total.tax_percentage}%), Discount: {total.discount_amount} ({total.discount_percentage}%), Total: {total.total_amount}"
                for total in totals
            ]
        )
