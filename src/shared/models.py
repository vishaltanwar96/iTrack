from django.db import models
from django.core import validators
from user.models import User


class AbstractIdName(models.Model):
    """
    Abstract Model for id name Models
    """

    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class AbstractRemarksHistory(models.Model):
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Status(AbstractIdName):
    class Meta:
        db_table = "status"


class Criticality(AbstractIdName):
    class Meta:
        db_table = "criticality"


class EntityMixin(models.Model):
    name = models.CharField(
        max_length=100,
        validators=(
            validators.MinLengthValidator(
                limit_value=2,
                message="Project name need to be atleast 2 characters long",
            ),
        ),
    )
    description = models.TextField(
        validators=(
            validators.MinLengthValidator(
                limit_value=10,
                message="Project description must be atleast 10 characters long",
            ),
        ),
    )
    criticality = models.ForeignKey(Criticality, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        abstract = True
