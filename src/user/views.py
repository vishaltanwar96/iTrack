from datetime import timedelta

from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core import signing

from .models import User
from .serializers import UserSerializer


class UserRegistrationView(CreateAPIView):
    """."""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """."""

        user = serializer.save()
        # THIS EMAIL MUST BE REPLACED WITH A CELERY TASK AND EMAIL MESSAGE WITH A HTML MESSAGE TEMPLATE
        user.email_user(
            "[ITRACK] ACCOUNT HAS BEEN CREATED",
            f"Greetings! {user.first_name.title()} {user.last_name.title()}\n\n Your iTrack user account has been created, Please follow the link below to verfiy/confirm your account\nhttp://127.0.0.1:8000/api/users/confirm/{signing.dumps(user.id)}/",
        )


class UserAccountConfirmationView(APIView):
    """."""

    permission_classes = [AllowAny]

    def get(self, request, signed_user_token):
        """."""

        try:
            user_id = signing.loads(signed_user_token, max_age=timedelta(days=2))
        except signing.SignatureExpired:
            return Response(
                {"msg": "Signature expired, please request a new one"},
                status.HTTP_400_BAD_REQUEST,
            )
        except signing.BadSignature:
            return Response({"msg": "Invalid signature"}, status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status.HTTP_400_BAD_REQUEST)
        if user.is_active:
            return Response(
                {"msg": "User account already confirmed"}, status.HTTP_409_CONFLICT
            )
        user.is_active = True
        user.save()
        user.email_user(
            "[ITRACK] ACCOUNT HAS BEEN CONFIRMED",
            f"Greetings! {user.first_name.title()} {user.last_name.title()}\n\n Your iTrack user account has been confirmed",
        )
        return Response(
            {
                "msg": "User acccount has been confirmed successfully",
                "data": UserSerializer(instance=user).data,
            },
            status.HTTP_200_OK,
        )
