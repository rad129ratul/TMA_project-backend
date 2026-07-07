from django.urls import path
from .views import (
    UploadedImageListCreateView,
    AnnotationListCreateView,
    AnnotationDeleteView,
)

urlpatterns = [
    path("images/", UploadedImageListCreateView.as_view(), name="image-list-create"),
    path("annotations/", AnnotationListCreateView.as_view(), name="annotation-list-create"),
    path("annotations/<int:pk>/", AnnotationDeleteView.as_view(), name="annotation-delete"),
]