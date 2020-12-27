from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from shared.models import Status
from itrack.permissions import IsAccessAllowedToGroup


class TaskViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAccessAllowedToGroup]

    def perform_create(self, serializer):
        """."""

        return serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """."""

        # move all constants like 'ASSIGNED' to a separate module when refactoring the project
        serializer = self.get_serializer(
            data={
                **request.data,
                "status": Status.objects.get(name="ASSIGNED").id,
                "assigned_by": request.user.id,
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
            subject="NEW TASK ALERT",
            message=f"Greetings!\n{assigned_to_user.first_name} {assigned_to_user.last_name},\nNew task has been assigned to you by {task.assigned_by.first_name} {task.assigned_by.last_name}\nDetails:\nTask ID: #{task.id}\nTask: {task.name}\n\nSincerely\niTrack",
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
