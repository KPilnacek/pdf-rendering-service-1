import pytest

from pdf_rendering_service.documents.models import Document
from pdf_rendering_service.documents.serializers import DocumentSerializer

pytestmark = pytest.mark.django_db


def test_document_serializer(document: Document):
    data = DocumentSerializer(document).data
    assert data["status"] == document.get_status_display()
