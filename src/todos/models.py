from django.db import models

from user.models import User


class Todo(models.Model):

    todo = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)

    class Meta:
        db_table = "todo"
