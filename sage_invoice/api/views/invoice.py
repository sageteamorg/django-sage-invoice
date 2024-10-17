from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from sage_invoice.api.helpers.versioning import HeaderVersioning
from sage_invoice.api.mixins import ErrorHandlingMixin
from sage_invoice.api.serializers import (
    ColumnSerializer,
    ExpenseSerializer,
    InvoiceSerializer,
    ItemSerializer,
)
from sage_invoice.models import Column, Expense, Invoice, Item


class InvoiceViewSet(ErrorHandlingMixin, viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = "slug"
    versioning_class = HeaderVersioning
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = (
        "title",
        "tracking_code",
        "customer_name",
    )
    filterset_fields = ("receipt", "status", "category")
    ordering_fields = ("invoice_date", "due_date")
    ordering = "-invoice_date"
