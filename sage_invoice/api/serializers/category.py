# serializers.py
from rest_framework import serializers

from sage_invoice.models import Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="category-detail", lookup_field="slug"
    )
    invoices = serializers.HyperlinkedRelatedField(
        many=True, view_name="invoice-detail", lookup_field="slug", read_only=True
    )

    class Meta:
        model = Category
        fields = ("url", "title", "description", "invoices")
        extra_kwargs = {
            "url": {"lookup_field": "slug"},
        }
