from django.db import models


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


class Status(AbstractIdName):
    class Meta:
        db_table = "status"


class Criticality(AbstractIdName):
    class Meta:
        db_table = "criticality"
