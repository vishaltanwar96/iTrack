from django.db import models

from user.models import User
from project.models import Project
from shared.models import AbstractEntity, AbstractRemarksHistory
from itrack.model_field_validation import past_date_validator


class Task(AbstractEntity):
    entity = "Task"
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="responsible"
    )
    assigned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator"
    )
    reviewed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewer", null=True
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # dependency limited to one person for now
    dependency = models.CharField(max_length=255, null=True)
    expected_completion_date = models.DateField(validators=[past_date_validator])
    actual_completion_date = models.DateField(
        null=True, validators=[past_date_validator]
    )

    class Meta:
        db_table = "task"


class TaskRemarksHistory(AbstractRemarksHistory):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        db_table = "task_remarks_history"
