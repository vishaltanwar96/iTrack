from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project, ProjectRemarksHistory
from .serializers import (
    ProjectSerializer,
    ProjectUsersSerializer,
    ProjectRemarksHistorySerializer,
)
from itrack.permissions import IsAccessAllowedToGroup

User = get_user_model()


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

    @action(
        methods=["post"],
        detail=True,
        url_path="associate-users",
        url_name="associate_users",
    )
    def associate_users_to_project(self, request, pk=None):
        """Associate users to current project"""

        project = self.get_object()
        serializer = ProjectUsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for user_id in serializer.validated_data["users"]:
            user = get_object_or_404(User, id=user_id)
            project.users.add(user)
            user.email_user(
                subject="WELCOME TO THE PROJECT",
                message=f"Greetings!\n{user.first_name} {user.last_name},\nWelcome to the Project-{project.name}, we look forward for your contribution\nSincerely\niTrack",
            )
        return Response(
            {"detail": "users have been associated with the project successfully"},
            status.HTTP_200_OK,
        )

    @action(
        methods=["post"],
        detail=True,
        url_path="remove-users",
        url_name="remove_users",
    )
    def remove_users_from_project(self, request, pk=None):
        """Remove users from current project"""

        project = self.get_object()
        serializer = ProjectUsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for user_id in serializer.validated_data["users"]:
            user = get_object_or_404(User, id=user_id)
            project.users.remove(user)
        return Response(
            {"detail": "users have been remove from the project successfully"},
            status.HTTP_200_OK,
        )

    # two actions defined on same url_path doesn't work will have to use something else for nested url relationships
    @action(
        methods=["post"],
        detail=True,
        url_path="remarks",
        url_name="remarks",
    )
    def add_remarks(self, request, pk=None):
        """Add remarks to current project"""

        project = self.get_object()
        serializer = ProjectRemarksHistorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ProjectRemarksHistory.objects.create(
            **serializer.validated_data,
            **{"project": project, "created_by": request.user},
        )
        return Response(
            {"detail": "remarks has been added to the project successfully"},
            status.HTTP_200_OK,
        )

    @action(
        methods=["get"],
        detail=True,
        url_path="remarks",
        url_name="remarks",
    )
    def fetch_remarks(self, request, pk=None):
        """Get all the remarks from current project"""

        remarks = ProjectRemarksHistory.objects.filter(project=self.get_object().id)
        serializer = ProjectRemarksHistorySerializer(instance=remarks, many=True)
        return Response(
            serializer.data,
            status.HTTP_200_OK,
        )
