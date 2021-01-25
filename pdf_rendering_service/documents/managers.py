from django.core.files.base import File
from django.db import models


class DocumentManager(models.Manager):
    def create_from_file(self, file: File):
        return self.create(
            original_name=file.name,
        )
