from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField

from pdf_rendering_service.documents.managers import DocumentManager


class Document(models.Model):
    PROCESSING, DONE = range(2)
    STATUSES = (
        (PROCESSING, "processing"),
        (DONE, "done"),
    )

    original_name = models.TextField(
        blank=True,
    )
    status = models.IntegerField(
        choices=STATUSES,
        default=PROCESSING,
        blank=True,
        db_index=True,
    )
    n_pages = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )
    created = CreationDateTimeField(_("created"))

    objects = DocumentManager()
