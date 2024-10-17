from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ColumnViewSet,
    ExpenseViewSet,
    InvoiceViewSet,
    ItemViewSet,
)

router = DefaultRouter()
router.register(r"expenses", ExpenseViewSet)
router.register(r"invoices", InvoiceViewSet)
router.register(r"items", ItemViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"columns", ColumnViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
