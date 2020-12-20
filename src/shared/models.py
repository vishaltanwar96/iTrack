from django.db import models
from django.core import validators
from user.models import User


class AbstractIdName(models.Model):
    """
    Abstract Model for id name Models
    """

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True


class AbstractRemarksHistory(models.Model):
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Status(AbstractIdName):
    class Meta:
        db_table = "status"

    def __str__(self):
        """."""

        return "%s" % (self.name,)


class Criticality(AbstractIdName):
    class Meta:
        db_table = "criticality"

    def __str__(self):
        """."""

        return "%s" % (self.name,)


class AbstractEntity(models.Model):
    entity = None
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=(
            validators.MinLengthValidator(
                limit_value=2,
                message=f"{entity} name need to be atleast 2 characters long",
            ),
        ),
    )
    description = models.TextField(
        validators=(
            validators.MinLengthValidator(
                limit_value=10,
                message=f"{entity} description must be atleast 10 characters long",
            ),
        ),
    )
    criticality = models.ForeignKey(Criticality, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
