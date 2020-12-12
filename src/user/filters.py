from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilterSet(filters.FilterSet):
    """."""

    class Meta:
        """."""

        model = User
        fields = {
            "email": ["icontains"],
            "first_name": ["iexact"],
            "last_name": ["iexact"],
            "id": ["exact"],
        }
