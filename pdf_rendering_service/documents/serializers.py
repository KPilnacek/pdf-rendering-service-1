from rest_framework import serializers

from pdf_rendering_service.documents.models import Document


class CreatedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id",)


class DocumentSerializer(serializers.ModelSerializer):

    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = Document
        fields = ("status", "n_pages")
