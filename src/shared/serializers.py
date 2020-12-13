from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Status, Criticality


class StatusSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Status
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Group
        fields = "__all__"


class CriticalitySerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Criticality
        fields = "__all__"
