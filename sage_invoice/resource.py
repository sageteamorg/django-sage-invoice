import json
from decimal import Decimal

from django.core.exceptions import ValidationError
from import_export import fields, resources
from import_export.widgets import BooleanWidget, DateWidget, ForeignKeyWidget, Widget

from sage_invoice.models import Category, Column, Expense, Invoice, Item


class JSONFieldWidget(Widget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError as err:
            raise ValidationError(f"Invalid JSON format in field: {value}") from err

    def render(self, value, obj=None):
        if value is None:
            return ""
        return json.dumps(value)


# ItemResource handles Invoice Items
class ItemResource(resources.ModelResource):
    invoice = fields.Field(
        column_name="invoice_id",
        attribute="invoice",
        widget=ForeignKeyWidget(Invoice, "id"),  # Use 'id' for foreign key lookup
    )

    class Meta:
        model = Item
        fields = (
            "id",
            "invoice",
            "description",
            "quantity",
            "unit_price",
            "total_price",
        )
        import_id_fields = ["id"]


# ColumnResource handles custom columns for invoices
class ColumnResource(resources.ModelResource):
    invoice = fields.Field(
        column_name="invoice_id",
        attribute="invoice",
        widget=ForeignKeyWidget(Invoice, "id"),
    )
    item = fields.Field(
        column_name="item_id",
        attribute="item",
        widget=ForeignKeyWidget(Item, "id"),
    )

    class Meta:
        model = Column
        fields = ("id", "invoice", "item", "column_name", "value", "priority")
        import_id_fields = ["id"]


class ExpenseResource(resources.ModelResource):
    invoice = fields.Field(
        column_name="invoice_id",
        attribute="invoice",
        widget=ForeignKeyWidget(Invoice, "id"),  # Use 'id' for foreign key lookup
    )

    class Meta:
        model = Expense
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


# CategoryResource handles Invoice Categories
class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "description",
        )
        import_id_fields = ["id"]


# Main InvoiceResource to handle invoice importing/exporting
class InvoiceResource(resources.ModelResource):
    notes = fields.Field(
        column_name="notes",
        attribute="notes",
        widget=JSONFieldWidget(),
    )

    contacts = fields.Field(
        column_name="contacts",
        attribute="contacts",
        widget=JSONFieldWidget(),
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
        column_name="receipt",
        attribute="receipt",
        widget=BooleanWidget(),
    )

    items = fields.Field()
    columns = fields.Field()
    totals = fields.Field()
    category = fields.Field()

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
            "contacts",
            "due_date",
            "tracking_code",
            "notes",
            "logo",
            "signature",
            "stamp",
            "template_choice",
            "category",
            "items",
            "columns",
            "totals",
        )
        import_id_fields = ["id"]

    def before_import_row(self, row, **kwargs):
        """
        Before importing, handle category, items, columns, and totals exactly like
        other fields.
        """
        # Initialize the invoice_item_map for each row import
        self.invoice_item_map = {}

        if row.get("items"):
            self.create_invoice_items(row["items"], row["id"])

        if row.get("columns"):
            self.create_invoice_columns(row["columns"], row["id"])

        if row.get("totals"):
            self.create_expenses(row["totals"], row["id"])

    def after_import_row(self, row, row_result, **kwargs):
        """After row import, assign the created or updated category to the invoice."""
        if row.get("category"):
            category_data = row["category"].split("|")
            title = category_data[0].strip()
            description = category_data[1].strip() if len(category_data) > 1 else ""

            # Create or update the Category
            category, created = Category.objects.update_or_create(
                title=title,
                defaults={"description": description},
            )

            # Now, directly set the category for the current invoice
            invoice = Invoice.objects.get(id=row["id"])
            invoice.category = category
            invoice.save()

    def create_invoice_items(self, items_data, invoice_id):
        items = items_data.split("; ")
        for item_data in items:
            try:
                description, quantity, unit_price, total_price = item_data.split("|")
                item, created = Item.objects.update_or_create(
                    invoice_id=invoice_id,
                    description=description.strip(),
                    defaults={
                        "quantity": int(quantity.strip()),
                        "unit_price": Decimal(unit_price.strip()),
                        "total_price": Decimal(total_price.strip()),
                    },
                )
                self.invoice_item_map[invoice_id] = item
            except ValueError as err:
                raise ValidationError(f"Invalid item data:{item_data}") from err

    def create_invoice_columns(self, columns_data, invoice_id):
        columns = columns_data.split("; ")
        for column_data in columns:
            try:
                column_name, value, count = column_data.split("|")
                item = self.invoice_item_map.get(invoice_id)
                if not item:
                    raise ValidationError(
                        f"No matching invoice item for invoice {invoice_id}"
                    )
                Column.objects.update_or_create(
                    invoice_id=invoice_id,
                    item=item,
                    column_name=column_name.strip(),
                    defaults={"value": value.strip(), "priority": count},
                )
            except ValueError as err:
                raise ValidationError(f"Invalid column data:{column_data}") from err

    def create_expenses(self, totals_data, invoice_id):
        try:
            (
                subtotal,
                tax_percentage,
                discount_percentage,
                concession_percentage,
            ) = totals_data.split("|")
            tax_amount = Decimal(subtotal) * (Decimal(tax_percentage) / 100)
            discount_amount = Decimal(subtotal) * (Decimal(discount_percentage) / 100)
            total_amount = (Decimal(subtotal) + tax_amount) - discount_amount

            Expense.objects.update_or_create(
                invoice_id=invoice_id,
                defaults={
                    "subtotal": Decimal(subtotal),
                    "tax_percentage": Decimal(tax_percentage),
                    "discount_percentage": Decimal(discount_percentage),
                    "tax_amount": tax_amount,
                    "discount_amount": discount_amount,
                    "total_amount": total_amount,
                },
            )
        except ValueError as err:
            raise ValidationError(f"Invalid totals data: {totals_data}") from err

    # Export related data for items, columns, totals, and contacts
    def dehydrate_items(self, invoice):
        items = Item.objects.filter(invoice=invoice)
        return "; ".join(
            [
                f"{item.description}|{item.quantity}|{item.unit_price}|{item.total_price}"
                for item in items
            ]
        )

    def dehydrate_columns(self, invoice):
        columns = Column.objects.filter(invoice=invoice)
        return "; ".join(
            [
                f"{column.column_name}|{column.value}|{column.priority}"
                for column in columns
            ]
        )

    def dehydrate_totals(self, invoice):
        totals = Expense.objects.filter(invoice=invoice)
        return "; ".join(
            [
                f"{total.subtotal}|{total.tax_percentage}|{total.discount_percentage}|{total.concession_percentage}"
                for total in totals
            ]
        )

    def dehydrate_category(self, invoice):
        """Export category data as 'title|description' format."""
        if invoice.category:
            return f"{invoice.category.title}|{invoice.category.description}"
        return ""

    def dehydrate_contacts(self, invoice):
        """Export contacts JSON field."""
        return json.dumps(invoice.contacts)
