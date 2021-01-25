from django.urls import include, path

urlpatterns = [
    path("", include("pdf_rendering_service.documents.urls", namespace="documents")),
]
