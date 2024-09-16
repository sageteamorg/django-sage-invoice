from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_tools.mixins.models import TitleSlugMixin


class Category(TitleSlugMixin):
    description = models.CharField(
        max_length=255,
        verbose_name=_("Description"),
        null=True,
        blank=True,
        help_text=_("Description of the Category."),
        db_comment="Description of the Category",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories ")
        db_table = "sage_invoice_cat"
