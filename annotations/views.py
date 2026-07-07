from rest_framework import generics, permissions
from .models import UploadedImage
from .serializers import UploadedImageSerializer


class UploadedImageListCreateView(generics.ListCreateAPIView):
    serializer_class = UploadedImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UploadedImage.objects.filter(uploaded_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)