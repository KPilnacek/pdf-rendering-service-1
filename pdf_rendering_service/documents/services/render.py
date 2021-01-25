import logging

from django.conf import settings
from pdf2image import convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
)
from PIL import Image
from resizeimage import resizeimage

from pdf_rendering_service.documents.models import Document
from pdf_rendering_service.documents.services.document_store import (
    get_document_file,
    store_document_page,
)

logger = logging.getLogger(__name__)


def render_document_into_png_files(document: Document):
    try:
        images = convert_from_bytes(get_document_file(document).read())
    except (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError) as e:
        logger.error(
            "PDF document id: %s could not be processed because of err: %s",
            document.id,
            e.__class__.__name__,
        )
        return

    for page_num, image in enumerate(images):
        image = normalize_document_page_image(image)
        store_document_page(document.id, page_num + 1, image)

    document.n_pages = len(images)
    document.status = Document.DONE
    document.save()


def normalize_document_page_image(image: Image) -> Image:
    # resize the image to fit the specified area keeping the ratio and without crop
    width, height = image.size
    if (
        width > settings.DOCUMENT_PAGE_IMAGE_MAX_WIDTH
        or height > settings.DOCUMENT_PAGE_IMAGE_MAX_HEIGHT
    ):
        return resizeimage.resize_contain(
            image,
            [
                settings.DOCUMENT_PAGE_IMAGE_MAX_WIDTH,
                settings.DOCUMENT_PAGE_IMAGE_MAX_HEIGHT,
            ],
        )
    return image
