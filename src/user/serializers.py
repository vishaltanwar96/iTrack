from django.core import exceptions
from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """."""

    confirm_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_password(password):
        """."""

        try:
            password_validation.validate_password(password)
        except exceptions.ValidationError as ve:
            raise serializers.ValidationError(ve.messages)
        return password

    def validate(self, attrs):
        """."""

        super(UserSerializer, self).validate(attrs)
        if attrs["password"] != attrs.pop("confirm_password"):
            raise serializers.ValidationError(
                {"password": ["password doesn't match confirm_password"]}
            )
        return attrs

    class Meta:
        """."""

        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            "groups": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "user_permissions": {"write_only": True},
        }
