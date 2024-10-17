# views.py
from rest_framework import viewsets

from sage_invoice.api.serializers import ColumnSerializer
from sage_invoice.models import Column


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
