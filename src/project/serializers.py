from rest_framework import serializers

from .models import Project, ProjectRemarksHistory


class ProjectSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = (
            "created_by",
            "created_at",
            "updated_at",
            "is_active",
        )
        extra_kwargs = {
            "created_by": {"default": serializers.CurrentUserDefault()},
        }


class ProjectUsersSerializer(serializers.Serializer):
    """."""

    users = serializers.ListField(
        child=serializers.IntegerField(min_value=1), allow_empty=False, min_length=1
    )


class ProjectRemarksHistorySerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = ProjectRemarksHistory
        fields = "__all__"
        ordering = ["-created_at"]
        read_only_fields = ("created_by",)
        extra_kwargs = {
            "created_by": {"default": serializers.CurrentUserDefault()},
        }
