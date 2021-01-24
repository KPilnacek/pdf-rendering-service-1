from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocumentsConfig(AppConfig):
    name = "pdf_rendering_service.documents"
    verbose_name = _("Documents")

    def ready(self):
        try:
            import pdf_rendering_service.documents.signals  # noqa F401
        except ImportError:
            pass
