from rest_framework import serializers

from .models import Project, ProjectRemarksHistory


class ProjectSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Project
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
                "read_only": True,
            },
        }
