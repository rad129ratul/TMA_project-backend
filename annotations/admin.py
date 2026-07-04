from django.contrib import admin
from .models import UploadedImage, Annotation


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'uploaded_at')


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'label', 'created_at')