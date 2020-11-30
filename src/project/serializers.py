from rest_framework import serializers

from .models import Project, ProjectRemarksHistory


class ProjectSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("created_by",)
        extra_kwargs = {
            "created_by": {"default": serializers.CurrentUserDefault()},
        }
