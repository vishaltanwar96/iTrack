from django.db import models

from user.models import User
from shared.models import AbstractRemarksHistory, AbstractEntity


class Project(AbstractEntity):
    entity = "Project"
    users = models.ManyToManyField(
        User,
        related_name="projects",
        related_query_name="projects",
    )

    class Meta:
        db_table = "project"
        ordering = ["id"]


class ProjectRemarksHistory(AbstractRemarksHistory):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = "project_remarks_history"
        ordering = ["id"]
