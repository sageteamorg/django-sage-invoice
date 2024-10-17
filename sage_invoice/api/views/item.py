# views.py
from rest_framework import viewsets

from sage_invoice.api.serializers import ItemSerializer
from sage_invoice.models import Item


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
