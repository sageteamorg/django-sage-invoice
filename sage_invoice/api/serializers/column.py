from rest_framework import serializers

from sage_invoice.models import Column


class ColumnSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Column
        fields = "__all__"
        lookup_field = "id"
        extra_kwargs = {
            "url": {"lookup_field": "id"},
            "invoice": {"lookup_field": "slug"},
            "item": {"lookup_field": "id"},
        }
