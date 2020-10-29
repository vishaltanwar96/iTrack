from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group


class Command(BaseCommand):
    """
    Add all relevant permissions to the group of users
    """

    help = "Add all relevant permissions to the group of users"
    perms = {
        "manager": [
            "add_project",
            "change_project",
            "delete_project",
            "view_project",
            "add_projectremarkshistory",
            "view_projectremarkshistory",
            "add_task",
            "change_task",
            "delete_task",
            "view_task",
            "add_taskremarkshistory",
            "view_taskremarkshistory",
            "add_todo",
            "change_todo",
            "delete_todo",
            "view_todo",
        ],
        "contributor": [
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
        ],
    }

    def add_arguments(self, parser):

        pass

    def handle(self, *args, **options):

        for group, permission_codes in self.perms.items():
            grp = Group.objects.get(name=group)
            for codename in permission_codes:
                permission = Permission.objects.get(codename=codename)
                grp.permissions.add(permission)
