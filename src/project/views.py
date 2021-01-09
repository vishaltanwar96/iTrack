from django.contrib.auth import get_user_model
from django.db import connection
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Project, ProjectRemarksHistory
from .filters import ProjectRemarksHistoryFilterSet
from .serializers import (
    ProjectSerializer,
    ProjectUsersSerializer,
    ProjectRemarksHistorySerializer,
)
from itrack.permissions import IsAccessAllowedToGroup
from itrack.communication_messages import EMAIL_BODY, EMAIL_SUBJECT

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAccessAllowedToGroup]
    NEW_PROJECT_ASSOCIATION_EVENT = "NEW_PROJECT_ASSOCIATION"

    project_task_metrics_query = """
        SELECT 
            status.id AS status_id,
            status.name AS status_name,
            COUNT(task.status_id) AS task_count
        FROM
            task
                RIGHT JOIN
            status ON task.status_id = status.id
        WHERE
            task.project_id = %s
                OR task.project_id IS NULL
        GROUP BY status.id;
    """

    def destroy(self, request, *args, **kwargs):
        """."""

        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """."""

        return self.request.user.projects.all()

    def perform_create(self, serializer):
        """."""

        serializer.save(created_by=self.request.user, users=[self.request.user.id])

    @action(
        methods=["get"],
        detail=True,
        url_path="metrics",
        url_name="task-metrics",
    )
    def task_metrics(self, request, pk=None):
        """Task metrics in current project"""

        # Could the equivalent be achieved in Django ORM query? Cuz this looks ugly :(

        project = self.get_object()
        with connection.cursor() as cursor:
            cursor.execute(self.project_task_metrics_query, [project.id])
            columns = [column_desciption[0] for column_desciption in cursor.description]
            project_task_metrics_data = [
                dict(zip(columns, project_task_metric))
                for project_task_metric in cursor.fetchall()
            ]

        return Response(project_task_metrics_data, status.HTTP_200_OK)

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
            if user in project.users.all():
                continue
            project.users.add(user)
            user.email_user(
                subject=EMAIL_SUBJECT[self.NEW_PROJECT_ASSOCIATION_EVENT],
                message=EMAIL_BODY[self.NEW_PROJECT_ASSOCIATION_EVENT].format(
                    user_first_name=user.first_name,
                    user_last_name=user.last_name,
                    project_name=project.name,
                ),
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
            if user == self.request.user:
                return Response(
                    {"detail": "You cannot remove yourself from the project"},
                    status.HTTP_400_BAD_REQUEST,
                )
            project.users.remove(user)
        return Response(
            {"detail": "users have been removed from the project successfully"},
            status.HTTP_200_OK,
        )


class ProjectRemarksHistoryViewSet(viewsets.ModelViewSet):
    """."""

    queryset = ProjectRemarksHistory.objects.all()
    permission_classes = [IsAccessAllowedToGroup]
    serializer_class = ProjectRemarksHistorySerializer
    filterset_class = ProjectRemarksHistoryFilterSet

    def perform_create(self, serializer):
        """."""

        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user not in serializer.validated_data["project"].users.all():
            raise PermissionDenied
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_queryset(self):
        """."""

        return self.queryset.filter(
            project__in=[project.id for project in self.request.user.projects.all()]
        )
