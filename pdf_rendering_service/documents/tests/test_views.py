from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from pdf_rendering_service.documents.models import Document
from pdf_rendering_service.documents.views import (
    DocumentPageView,
    DocumentUploadView,
    DocumentView,
)

pytestmark = pytest.mark.django_db


@patch("pdf_rendering_service.documents.views.store_document")
@patch("pdf_rendering_service.documents.views.process_document")
def test_document_upload(
    mock_process_document,
    mock_store_document,
    document_file_path,
    api_rf: APIRequestFactory,
):
    mock_process_document.send = Mock()
    with open(document_file_path, "rb") as f:
        request = api_rf.post(
            reverse("documents:documents"),
            f.read(),
            content_type="application/pdf",
            HTTP_CONTENT_DISPOSITION="attachment; filename='document.pdf'",
        )
    response = DocumentUploadView.as_view()(request)
    mock_store_document.assert_called_once()
    mock_process_document.send.assert_called_once()
    assert response.data["id"] > 0
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_document_get(document: Document, api_rf: APIRequestFactory):
    request = api_rf.get("fake_path")
    response = DocumentView.as_view()(request, pk=document.pk)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == document.get_status_display()
    response = DocumentView.as_view()(request, pk=document.pk + 1)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch("pdf_rendering_service.documents.views.get_document_page")
def test_document_page_get(
    mock_get_document_page, document: Document, api_rf: APIRequestFactory
):
    mock_get_document_page.return_value = Mock()
    view = DocumentPageView.as_view()
    request = api_rf.get("fake_path")
    kwargs = {"pk": document.pk, "number": 1}
    response = view(request, **kwargs)
    assert response.status_code == status.HTTP_200_OK
    mock_get_document_page.side_effect = FileNotFoundError
    response = view(request, **kwargs)
    assert response.status_code == status.HTTP_404_NOT_FOUND
