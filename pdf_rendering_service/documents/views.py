from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from pdf_rendering_service.documents.models import Document
from pdf_rendering_service.documents.renderers import PNGRenderer
from pdf_rendering_service.documents.serializers import (
    CreatedDocumentSerializer,
    DocumentSerializer,
)
from pdf_rendering_service.documents.services.document_store import (
    get_document_page,
    store_document,
)
from pdf_rendering_service.documents.tasks import process_document


class DocumentUploadView(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = (AllowAny,)

    def post(self, request, filename: str = ""):
        file = request.data["file"]
        document = store_document(file)
        process_document.send(document.pk)
        return Response(
            data=CreatedDocumentSerializer(document).data,
            status=status.HTTP_201_CREATED,
        )


class DocumentView(RetrieveAPIView):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    permission_classes = (AllowAny,)


class DocumentPageView(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = Document.objects.all()
    renderer_classes = (PNGRenderer,)

    def get(self, request, pk: int, number: str):
        document = self.get_object()
        try:
            image_file = get_document_page(document.pk, number)
        except FileNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data=image_file.read())
