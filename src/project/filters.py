from django_filters import rest_framework as filters

from .models import ProjectRemarksHistory


class ProjectRemarksHistoryFilterSet(filters.FilterSet):
    """."""

    class Meta:
        model = ProjectRemarksHistory
        fields = ["project"]
