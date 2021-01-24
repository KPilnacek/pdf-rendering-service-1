from unittest.mock import Mock, patch

import pytest
from django.core.files import File

from pdf_rendering_service.documents.models import Document
from pdf_rendering_service.documents.services.document_store import store_document
from pdf_rendering_service.documents.services.render import (
    render_document_into_png_files,
)

pytestmark = pytest.mark.django_db


@patch("pdf_rendering_service.documents.services.document_store.default_storage")
def test_store_document(mock_default_storage):
    mock_default_storage.save = Mock()
    file = File(b"")
    file.name = "foo"
    document = store_document(file)
    assert document.id is not None
    mock_default_storage.save.assert_called_once()
    document.delete()


@patch("pdf_rendering_service.documents.services.render.get_document_file")
@patch("pdf_rendering_service.documents.services.render.normalize_document_page_image")
@patch("pdf_rendering_service.documents.services.render.store_document_page")
def test_render_document_into_png_files(
    mock_store_document_page,
    mock_normalize_document_page_image,
    mock_get_document_file,
    document_file_path: str,
    document: Document,
):
    mock_get_document_file.return_value = File(open(document_file_path, "rb"))
    render_document_into_png_files(document)
    assert document.n_pages == 4
    assert document.status == Document.DONE
    mock_normalize_document_page_image.assert_called()
    mock_store_document_page.assert_called()


def test_normalize_document_page_image():
    # FIXME maybe in the future
    pass
