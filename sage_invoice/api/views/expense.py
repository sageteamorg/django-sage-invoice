# views.py
from rest_framework import viewsets
from sage_invoice.models import Expense
from sage_invoice.api.serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
