from django.urls import path

from pdf_rendering_service.documents.views import (
    DocumentPageView,
    DocumentUploadView,
    DocumentView,
)

app_name = "documents"

urlpatterns = [
    path("documents", DocumentUploadView.as_view(), name="documents"),
    path("documents/<int:pk>", DocumentView.as_view(), name="document"),
    path(
        "documents/<str:filename>",
        DocumentUploadView.as_view(),
        name="documents_with_filename",
    ),
    path(
        "documents/<int:pk>/pages/<int:number>",
        DocumentPageView.as_view(),
        name="document_page",
    ),
]
