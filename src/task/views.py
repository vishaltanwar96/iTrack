from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer

from shared.models import Status


class TaskViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_create(self, serializer):
        """."""

        return serializer.save()

    def create(self, request, *args, **kwargs):
        """."""

        # move all constants like 'ASSIGNED' to a separate module when refactoring the project
        serializer = self.get_serializer(
            data={
                **request.data,
                "status": Status.objects.get(name="ASSIGNED").id,
                "created_by": request.user.id,
                "assigned_by": request.user.id,
            }
        )
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["project"] not in request.user.projects.all():
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
