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


class PasswordResetEmailSerializer(serializers.Serializer):
    """."""

    email = serializers.EmailField(required=True)


class PasswordResetChangeSerializer(serializers.Serializer):
    """."""

    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    # Find a way such that methods below can be inherited in UserSerializer since the signature is almost same
    # Only varible name difference is there
    # (Can be achieved if the new_password -> password and confirm_new_password -> confirm_password)
    @staticmethod
    def validate_new_password(new_password):
        """."""

        try:
            password_validation.validate_password(new_password)
        except exceptions.ValidationError as ve:
            raise serializers.ValidationError(ve.messages)
        return new_password

    def validate(self, attrs):
        """."""

        super(PasswordResetChangeSerializer, self).validate(attrs)
        if attrs["new_password"] != attrs.pop("confirm_new_password"):
            raise serializers.ValidationError(
                {"new_password": ["new_password doesn't match confirm_new_password"]}
            )
        return attrs
