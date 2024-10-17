# serializers.py
from rest_framework import serializers

from sage_invoice.models import Expense


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"
        lookup_field = "id"
        extra_kwargs = {
            "url": {"lookup_field": "id"},
            "invoice": {"lookup_field": "slug"},
        }
