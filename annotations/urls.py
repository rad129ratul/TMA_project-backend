from django.urls import path
from .views import (
    UploadedImageListCreateView,
    AnnotationListCreateView,
    AnnotationDetailView,
)

urlpatterns = [
    path("images/", UploadedImageListCreateView.as_view(), name="image-list-create"),
    path("annotations/", AnnotationListCreateView.as_view(), name="annotation-list-create"),
    path("annotations/<int:pk>/", AnnotationDetailView.as_view(), name="annotation-detail"),
]