from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """."""

    class Meta:

        model = Todo
        fields = "__all__"
        read_only_fields = ("belongs_to", "is_complete", "created_at", "updated_at")
        extra_kwargs = {
            "belongs_to": {"default": serializers.CurrentUserDefault()},
        }
