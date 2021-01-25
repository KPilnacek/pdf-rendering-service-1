import os

import dramatiq
import pytest
from django.core.files.base import File
from django.core.files.storage import default_storage
from pytest_django.lazy_django import skip_if_no_django

from pdf_rendering_service.documents.models import Document


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def api_rf():
    skip_if_no_django()
    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()


@pytest.fixture
def broker():
    broker = dramatiq.get_broker()
    broker.flush_all()
    return broker


@pytest.fixture
def worker(broker):
    worker = dramatiq.Worker(broker, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()


@pytest.fixture
def document_file_path(settings) -> str:
    return os.path.join(settings.APPS_DIR, "documents/tests/data/document.pdf")


@pytest.fixture
def document_page_img_file_path(settings) -> str:
    return os.path.join(settings.APPS_DIR, "documents/tests/data/image.png")


@pytest.fixture
def document() -> Document:
    document = Document.objects.create(original_name="foo.pdf")
    yield document
    document.delete()


@pytest.fixture
def document_page_img_file(document_page_img_file_path: str) -> File:
    return File(default_storage.open(document_page_img_file_path))
