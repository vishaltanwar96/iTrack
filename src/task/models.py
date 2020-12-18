from django.db import models

from user.models import User
from project.models import Project
from shared.models import EntityMixin, AbstractRemarksHistory


class Task(EntityMixin):
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="responsible", null=True
    )
    assigned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="creator", null=True
    )
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="reviewer", null=True
    )
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    dependency = models.CharField(max_length=255, default=None)
    expected_completion_date = models.DateField()
    actual_completion_date = models.DateField(null=True)

    class Meta:
        db_table = "task"


class TaskRemarksHistory(AbstractRemarksHistory):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "task_remarks_history"
