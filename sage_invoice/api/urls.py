from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ExpenseViewSet,
    InvoiceViewSet,
    ItemViewSet,
    CategoryViewSet,
    ColumnViewSet
)

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'items', ItemViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'columns', ColumnViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
