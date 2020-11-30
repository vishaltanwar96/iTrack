from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer
from itrack.permissions import IsAccessAllowedToGroup


class ProjectViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAccessAllowedToGroup]

    def perform_create(self, serializer):
        """."""

        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """."""

        serializer = self.get_serializer(
            data={**request.data, "users": [request.user.id]}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
