from rest_framework import serializers

from .category import CategorySerializer
from .column import ColumnSerializer
from .item import ItemSerializer
from .expense import ExpenseSerializer

from sage_invoice.models import Invoice


class ContactFieldSerializer(serializers.Serializer):
    """
    Serializer to validate the structure of the contacts field (either phone or
    email).
    """

    phone = serializers.RegexField(
        regex=r"^\d{10,15}$",
        required=False,
        help_text="Phone number should only contain digits and be 10-15 characters long.",
    )
    email = serializers.EmailField(required=False, help_text="Valid email format.")

    def validate(self, data):
        """Ensure at least one of 'phone' or 'email' is provided."""
        if not data.get("phone") and not data.get("email"):
            raise serializers.ValidationError("Either phone or email must be provided.")
        return data


class NoteFieldSerializer(serializers.Serializer):
    """Serializer to validate the structure of the notes field (additional fields)."""

    label = serializers.CharField()
    content = serializers.CharField()


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    contacts = ContactFieldSerializer(required=False)
    notes = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()), required=False
    )
    category = CategorySerializer(read_only=True)
    items = ItemSerializer(many=True, read_only=True)
    columns = ColumnSerializer(many=True, read_only=True)
    expense = ExpenseSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "url",
            "slug",
            "invoice_date",
            "customer_name",
            "tracking_code",
            "contacts",
            "status",
            "receipt",
            "notes",
            "currency",
            "due_date",
            "template_choice",
            "logo",
            "signature",
            "stamp",
            "category",
            "items",
            "columns",
            "expense",
        ]
        extra_kwargs = {
            "url": {"lookup_field": "slug"},
            "categories": {"lookup_field": "slug"},
            "items": {"lookup_field": "id"},
            "columns": {"lookup_field": "id"},
            "expense": {"lookup_field": "id"},
        }
        read_only_fields = ["slug"]
