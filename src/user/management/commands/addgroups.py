from django.contrib.auth.models import Group
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Add groups (Roles) to be used by the application
    """

    def add_arguments(self, parser):

        parser.add_argument("name", type=str, nargs="+")

    def handle(self, *args, **options):

        for name in options["name"]:
            try:
                Group.objects.create(name=name)
            except IntegrityError:
                raise CommandError("Group(s) already exists.")
