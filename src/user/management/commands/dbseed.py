from django.db.utils import IntegrityError
from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand

from shared.models import Status, Criticality
from itrack import constants


class Command(BaseCommand):
    """
    Add all relevant permissions to the group of users
    """

    help = "Add all relevant permissions to the group of users"

    def add_arguments(self, parser):

        pass

    @staticmethod
    def add_entites(entities, entity_model):
        for entity in entities:
            try:
                entity_model.objects.create(name=entity)
            except IntegrityError:
                continue

    @staticmethod
    def add_group_perms():
        for group, permission_codes in constants.perms.items():
            grp = Group.objects.get(name=group)
            for codename in permission_codes:
                permission = Permission.objects.get(codename=codename)
                grp.permissions.add(permission)

    def handle(self, *args, **options):

        self.add_entites(constants.groups, Group)
        self.add_entites(constants.statuses, Status)
        self.add_entites(constants.criticalities, Criticality)
        self.add_group_perms()
