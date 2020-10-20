from django.db import models

from user.models import User
from shared.models import AbstractRemarksHistory, EntityMixin


class Project(EntityMixin):
    users = models.ManyToManyField(
        User,
        related_name="user_set",
        related_query_name="user_set",
    )

    class Meta:
        db_table = "project"


class ProjectRemarksHistory(AbstractRemarksHistory):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "project_remarks_history"
