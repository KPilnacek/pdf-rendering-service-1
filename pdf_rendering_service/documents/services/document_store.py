import os
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile, File
from django.core.files.storage import default_storage
from PIL import Image

from pdf_rendering_service.documents.models import Document


def store_document(document_file: File) -> Document:
    document = Document.objects.create_from_file(document_file)
    path = get_document_path(document.id)
    default_storage.save(path, document_file)
    return document


def get_document_file(document: Document) -> File:
    path = get_document_path(document.id)
    return default_storage.open(path)


def store_document_page(document_id: int, page_number: int, page_img: Image):
    buffer = BytesIO()
    page_img.save(fp=buffer, format="PNG")
    path = get_document_page_path(document_id, page_number)
    default_storage.save(path, ContentFile(buffer.getvalue()))


def get_document_page(document_id: int, page_number: int) -> File:
    path = get_document_page_path(document_id, page_number)
    if not default_storage.exists(path):
        raise FileNotFoundError
    return File(default_storage.open(path))


def get_document_path(document_id: int) -> str:
    return os.path.join(get_document_folder_path(document_id), f"{document_id}.pdf")


def get_document_folder_path(document_id: int) -> str:
    return os.path.join(settings.MEDIA_ROOT, settings.DOCUMENTS_DIR, str(document_id))


def get_document_page_path(document_id: int, page_number: int) -> str:
    return os.path.join(get_document_folder_path(document_id), f"{page_number}.png")
