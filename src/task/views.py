from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from shared.models import Status
from itrack import constants
from itrack.permissions import IsAccessAllowedToGroup
from itrack.communication_messages import EMAIL_BODY, EMAIL_SUBJECT


class TaskViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAccessAllowedToGroup]

    def perform_create(self, serializer):
        """."""

        return serializer.save(
            created_by=self.request.user, assigned_by=self.request.user
        )

    def list(self, request, *args, **kwargs):
        """."""

        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.filter(assigned_to=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """."""

        serializer = self.get_serializer(
            data={
                **request.data,
                "status": Status.objects.get(name=constants.ASSIGNED).id,
            }
        )
        serializer.is_valid(raise_exception=True)
        project = serializer.validated_data["project"]
        if not all(
            user in project.users.all()
            for user in [request.user, serializer.validated_data["assigned_to"]]
        ):
            raise exceptions.PermissionDenied
        assigned_to_user = serializer.validated_data["assigned_to"]
        task = self.perform_create(serializer)
        assigned_to_user.email_user(
            subject=EMAIL_SUBJECT[constants.NEW_TASK],
            message=EMAIL_BODY[constants.NEW_TASK].format(
                assignee_first_name=assigned_to_user.first_name,
                assignee_last_name=assigned_to_user.last_name,
                assignor_first_name=task.assigned_by.first_name,
                assignor_last_name=task.assigned_by.last_name,
                task_id=task.id,
                task_name=task.name,
            ),
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_queryset(self):
        """."""

        return self.queryset.filter(
            project__in=[project for project in self.request.user.projects.all()]
        )

    def destroy(self, request, *args, **kwargs):
        """."""

        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
