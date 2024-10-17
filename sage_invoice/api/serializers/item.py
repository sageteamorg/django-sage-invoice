# serializers.py
from rest_framework import serializers
from sage_invoice.models import Item


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        lookup_field = "id"
        extra_kwargs = {
            'url': {'lookup_field': 'id'},
            'invoice': {'lookup_field': "slug"}
        }
