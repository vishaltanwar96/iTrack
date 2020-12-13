from rest_framework import generics, permissions
from django.contrib.auth.models import Group

from .models import Status, Criticality
from .serializers import StatusSerializer, CriticalitySerializer, GroupSerializer


class StatusView(generics.ListAPIView):
    """."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class GroupView(generics.ListAPIView):
    """."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CriticalityView(generics.ListAPIView):
    """."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Criticality.objects.all()
    serializer_class = CriticalitySerializer
