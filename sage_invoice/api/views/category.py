from rest_framework import viewsets

from sage_invoice.api.helpers.versioning import HeaderVersioning
from sage_invoice.api.mixins import ErrorHandlingMixin
from sage_invoice.api.serializers import CategorySerializer
from sage_invoice.models import Category


class CategoryViewSet(ErrorHandlingMixin, viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related("invoices").all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

    versioning_class = HeaderVersioning

    def get_serializer_class(self):
        version = getattr(self.request, "version", None)

        if version == "1.0":
            return CategorySerializer

        return super().get_serializer_class()
