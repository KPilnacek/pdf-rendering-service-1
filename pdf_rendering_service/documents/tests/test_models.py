import pytest

from pdf_rendering_service.documents.models import Document

pytestmark = pytest.mark.django_db


def test_status_lbl_display(document: Document):
    assert document.get_status_display() == dict(Document.STATUSES)[Document.PROCESSING]
