from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _

from .managers import ITRACKUserManager


class User(AbstractUser):
    """
    iTrack User model on top of django's built-in user model
    """

    username = None
    group_display = "group"
    USERNAME_FIELD = "email"
    objects = ITRACKUserManager()
    REQUIRED_FIELDS = []
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=150)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_("Designates whether this user should be treated as active. "),
    )
    groups = models.ForeignKey(
        Group,
        db_column="%s_id" % group_display,
        verbose_name=_("%s" % group_display),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta(AbstractUser.Meta):
        db_table = "user"
