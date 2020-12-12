from django.db.models import QuerySet
from rest_framework import viewsets, permissions

from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """."""

    permission_classes = [permissions.DjangoObjectPermissions]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def perform_create(self, serializer):
        """."""

        serializer.save(belongs_to=self.request.user)

    def get_queryset(self):
        """."""

        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method." % self.__class__.__name__
        )

        queryset = self.queryset
        queryset = queryset.filter(belongs_to=self.request.user)
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset
