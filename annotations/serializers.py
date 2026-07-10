from rest_framework import serializers
from .models import UploadedImage, Annotation


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ["id", "task", "file", "uploaded_by", "uploaded_at"]
        read_only_fields = ["id", "uploaded_by", "uploaded_at"]

    def validate_task(self, value):
        # No user can attach images to another user's task.
        request = self.context.get("request")
        if request and value.owner_id != request.user.id:
            raise serializers.ValidationError("You do not own this task.")
        return value


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ["id", "image", "points", "label", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_points(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Points must be a list of coordinate pairs.")

        if len(value) < 3:
            raise serializers.ValidationError("A polygon requires at least 3 points.")

        for point in value:
            if not isinstance(point, dict) or "x" not in point or "y" not in point:
                raise serializers.ValidationError(
                    "Each point must be an object with 'x' and 'y' keys."
                )
            x, y = point["x"], point["y"]
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise serializers.ValidationError("Coordinate values must be numbers.")
            if not (0.0 <= x <= 1.0) or not (0.0 <= y <= 1.0):
                raise serializers.ValidationError(
                    "Coordinates must be normalized between 0.0 and 1.0."
                )

        return value

    def validate_image(self, value):
        request = self.context.get("request")
        if request and value.uploaded_by_id != request.user.id:
            raise serializers.ValidationError("You do not own this image.")
        return value