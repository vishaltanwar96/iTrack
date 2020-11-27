from django.db.utils import IntegrityError
from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand

from shared.models import Status, Criticality


class Command(BaseCommand):
    """
    Add all relevant permissions to the group of users
    """

    help = "Add all relevant permissions to the group of users"

    MANAGER = "MANAGER"
    CONTRIBUTOR = "CONTRIBUTOR"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    SEVERE = "SEVERE"
    ASSIGNED = "ASSIGNED"
    WIP = "WIP"
    ONHOLD = "ONHOLD"
    INREVIEW = "IN-REVIEW"
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"
    PLANNED = "PLANNED"

    groups = (MANAGER, CONTRIBUTOR)
    criticalities = (LOW, MEDIUM, HIGH, SEVERE)
    statuses = (
        ASSIGNED,
        WIP,
        ONHOLD,
        INREVIEW,
        SCHEDULED,
        COMPLETED,
        ABANDONED,
        PLANNED,
    )

    common_perms = [
        "view_project",
        "add_projectremarkshistory",
        "view_projectremarkshistory",
        "add_task",
        "view_task",
        "add_taskremarkshistory",
        "view_taskremarkshistory",
        "add_todo",
        "change_todo",
        "delete_todo",
        "view_todo",
    ]
    perms = {
        MANAGER: [
            "add_project",
            "change_project",
            "delete_project",
            "change_task",
            "delete_task",
        ]
        + common_perms,
        CONTRIBUTOR: common_perms,
    }

    def add_arguments(self, parser):

        pass

    @staticmethod
    def add_entites(entities, entity_model):
        for entity in entities:
            try:
                entity_model.objects.create(name=entity)
            except IntegrityError:
                continue

    def add_group_perms(self):
        for group, permission_codes in self.perms.items():
            grp = Group.objects.get(name=group)
            for codename in permission_codes:
                permission = Permission.objects.get(codename=codename)
                grp.permissions.add(permission)

    def handle(self, *args, **options):

        self.add_entites(self.groups, Group)
        self.add_entites(self.statuses, Status)
        self.add_entites(self.criticalities, Criticality)
        self.add_group_perms()
