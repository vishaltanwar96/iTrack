from rest_framework import serializers
from rest_framework.utils import model_meta

from .models import Task
from itrack import constants
from itrack.communication_messages import EMAIL_SUBJECT, EMAIL_BODY


class TaskSerializer(serializers.ModelSerializer):
    """."""

    def update(self, instance, validated_data):
        """."""

        serializers.raise_errors_on_nested_writes("update", self, validated_data)
        info = model_meta.get_field_info(instance)
        old_assignee = instance.assigned_to
        assignor = self.context["request"].user

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
            if attr == "assigned_to" and value != old_assignee:
                value.email_user(
                    subject=EMAIL_SUBJECT[constants.TASK_HANDOVER],
                    message=EMAIL_BODY[constants.TASK_HANDOVER].format(
                        new_assignee_first_name=value.first_name,
                        new_assignee_last_name=value.last_name,
                        old_assignee_first_name=old_assignee.first_name,
                        old_assignee_last_name=old_assignee.last_name,
                        assignor_first_name=assignor.first_name,
                        assignor_last_name=assignor.last_name,
                        task_id=instance.id,
                        task_name=instance.name,
                    ),
                )
                instance.assigned_by = assignor
        instance.save()

        return instance

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "created_by",
            "updated_at",
            "actual_completion_date",
            "reviewed_by",
            "is_active",
        )
