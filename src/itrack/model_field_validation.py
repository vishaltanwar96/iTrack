from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


def past_date_validator(value):
    """Checks if the date is less than current date"""

    if value < timezone.now().astimezone().date():
        raise ValidationError(_("cannot be less than current date"))
