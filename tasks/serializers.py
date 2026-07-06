from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "priority",
            "due_date",
            "tags",
            "status",
            "owner",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title is required.")
        return value.strip()

    def validate_priority(self, value):
        valid_priorities = [choice[0] for choice in Task.Priority.choices]
        if value not in valid_priorities:
            raise serializers.ValidationError(
                f"Priority must be one of {valid_priorities}."
            )
        return value

    def validate_due_date(self, value):
        if not value:
            raise serializers.ValidationError("Due date is required.")
        return value