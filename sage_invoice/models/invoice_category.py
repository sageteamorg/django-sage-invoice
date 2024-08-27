from django.db import models
from django.utils.translation import gettext_lazy as _
from sage_tools.mixins.models import TitleSlugMixin


class InvoiceCategory(TitleSlugMixin):
    description = models.CharField(
        max_length=255,
        verbose_name=_("Description"),
        help_text=_("Description of the Category."),
        db_comment="The description of the category",
    )

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Invoice Category")
        verbose_name_plural = _("Invoice Categories ")
        db_table = "sage_invoice_category"
