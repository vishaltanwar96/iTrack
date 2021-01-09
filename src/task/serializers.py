from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "created_by",
            "updated_at",
            "actual_completion_date",
            "reviewed_by",
        )
