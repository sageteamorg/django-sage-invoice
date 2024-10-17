from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from sage_invoice.models import Invoice
from sage_invoice.api.mixins import ErrorHandlingMixin
from sage_invoice.api.serializers import InvoiceSerializer, ColumnSerializer, ItemSerializer, ExpenseSerializer
from sage_invoice.api.helpers.versioning import HeaderVersioning
from sage_invoice.models import Column, Item, Expense


class InvoiceViewSet(ErrorHandlingMixin, viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'slug'
    versioning_class = HeaderVersioning
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = (
        'title',
        'tracking_code',
        'customer_name',
    )
    filterset_fields = (
        "receipt",
        "status",
        "category"
    )
    ordering_fields = (
        "invoice_date",
        "due_date"
    )
    ordering = (
        '-invoice_date'
    )
