from django.urls import resolve, reverse


def test_document_url():
    assert reverse("documents:documents") == "/documents"
    assert resolve("/documents").view_name == "documents:documents"


def test_document_with_filename_url():
    filename = "foo"
    assert (
        reverse("documents:documents_with_filename", kwargs={"filename": filename})
        == f"/documents/{filename}"
    )
    assert (
        resolve(f"/documents/{filename}").view_name
        == "documents:documents_with_filename"
    )
