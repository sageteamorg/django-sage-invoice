from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_tools.mixins.models import TitleSlugDescriptionMixin


class Category(TitleSlugDescriptionMixin):
    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories ")
        db_table = "sage_invoice_cat"
