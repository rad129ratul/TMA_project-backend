from django.db import models
from django.conf import settings


class UploadedImage(models.Model):
    file = models.ImageField(upload_to='images/')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_images',
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image #{self.pk} by {self.uploaded_by}"


class Annotation(models.Model):
    image = models.ForeignKey(
        UploadedImage,
        on_delete=models.CASCADE,   # Image ডিলিট হলে তার সব annotation ও ডিলিট হবে — orphan রেকর্ড এড়াতে
        related_name='annotations',
    )
    # points: normalized (0.0 - 1.0) x,y coordinate pairs, e.g. [{"x": 0.12, "y": 0.34}, ...]
    points = models.JSONField()
    label = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Annotation #{self.pk} on Image #{self.image_id}"