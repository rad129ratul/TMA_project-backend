from rest_framework import generics, permissions
from .models import UploadedImage, Annotation
from .serializers import UploadedImageSerializer, AnnotationSerializer


class UploadedImageListCreateView(generics.ListCreateAPIView):
    serializer_class = UploadedImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UploadedImage.objects.filter(uploaded_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class AnnotationListCreateView(generics.ListCreateAPIView):
    serializer_class = AnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Annotation.objects.filter(image__uploaded_by=self.request.user)

        image_id = self.request.query_params.get("image")
        if image_id:
            queryset = queryset.filter(image_id=image_id)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class AnnotationDeleteView(generics.DestroyAPIView):
    serializer_class = AnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Annotation.objects.filter(image__uploaded_by=self.request.user)