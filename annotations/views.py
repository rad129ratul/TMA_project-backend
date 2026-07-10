from rest_framework import generics, permissions
from .models import UploadedImage, Annotation
from .serializers import UploadedImageSerializer, AnnotationSerializer


class UploadedImageListCreateView(generics.ListCreateAPIView):
    serializer_class = UploadedImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ?task=<id> filter will be mandatory if sent
        queryset = UploadedImage.objects.filter(uploaded_by=self.request.user)

        task_id = self.request.query_params.get("task")
        if task_id:
            queryset = queryset.filter(task_id=task_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def get_serializer_context(self):
        # Passing context is mandatory to access request.user in validate_task()
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


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

# RetrieveUpdateDestroyAPIView (GET + PATCH/PUT + DELETE) — to support label editing
class AnnotationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ownership filter unchanged — 404 when trying to edit/delete another user's annotation
        return Annotation.objects.filter(image__uploaded_by=self.request.user)

    def get_serializer_context(self):
        # PATCH also requires request.user in the validate_image() serializer method
        context = super().get_serializer_context()
        context["request"] = self.request
        return context