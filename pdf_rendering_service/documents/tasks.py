import logging

import dramatiq

from pdf_rendering_service.documents.models import Document
from pdf_rendering_service.documents.services.render import (
    render_document_into_png_files,
)

logger = logging.getLogger(__name__)


@dramatiq.actor
def process_document(document_id: int):
    logger.info("Processing document id: %s STARTED", document_id)
    document = Document.objects.get(pk=document_id)
    render_document_into_png_files(document)
    logger.info("Processing document id: %s DONE", document_id)
