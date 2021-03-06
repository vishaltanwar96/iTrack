from datetime import timedelta

from django.core import signing
from django.contrib.auth import get_user_model
from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from itrack import constants
from itrack.communication_messages import EMAIL_BODY, EMAIL_SUBJECT


from .serializers import (
    UserSerializer,
    EmailSerializer,
    PasswordResetChangeSerializer,
)
from .filters import UserFilterSet
from itrack.permissions import IsAccessAllowedToGroup

User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    """."""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """."""

        user = serializer.save()
        # THIS EMAIL MUST BE REPLACED WITH A CELERY TASK AND EMAIL MESSAGE WITH A HTML MESSAGE TEMPLATE
        # SEND USER ONLY THE ACTIVATION CODE THAT THEY'LL ENTER ON THE WEBSITE TO ACTIVATE THEIR ACCOUNT
        user.email_user(
            subject=EMAIL_SUBJECT[constants.USER_ACCOUNT_CREATED],
            message=EMAIL_BODY[constants.USER_ACCOUNT_CREATED].format(
                user_first_name=user.first_name,
                user_last_name=user.last_name,
                secret_key_signed_code=signing.dumps(user.id),
            ),
        )


class ResendActivationEmailView(views.APIView):
    """Resend activation code to the user again on their email"""

    permission_classes = [AllowAny]
    serializer_class = EmailSerializer

    def post(self, request):
        """."""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid email, not found"}, status.HTTP_404_NOT_FOUND
            )
        if user.is_active:
            return Response(
                {"detail": "User account already active"}, status.HTTP_400_BAD_REQUEST
            )
        user.email_user(
            subject=EMAIL_SUBJECT[constants.RESEND_ACTIVATION_CODE],
            message=EMAIL_BODY[constants.RESEND_ACTIVATION_CODE].format(
                user_first_name=user.first_name,
                user_last_name=user.last_name,
                secret_key_signed_code=signing.dumps(user.id),
            ),
        )
        return Response(
            {"detail": "Activation code has been sent successfully."},
            status.HTTP_200_OK,
        )


class AccountConfirmationView(views.APIView):
    """."""

    permission_classes = [AllowAny]

    def post(self, request, signed_user_token):
        """."""

        # signed_user_token validation can be placed in utilities helper functions to validate a token.
        try:
            user_id = signing.loads(signed_user_token, max_age=timedelta(days=2))
            user = User.objects.get(id=user_id)
        except signing.SignatureExpired:
            return Response(
                {"detail": "Signature expired, please request a new one"},
                status.HTTP_400_BAD_REQUEST,
            )
        except signing.BadSignature:
            return Response(
                {"detail": "Invalid signature"}, status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response(
                {"detail": "User account already confirmed"}, status.HTTP_409_CONFLICT
            )
        user.is_active = True
        user.save()
        user.email_user(
            subject=EMAIL_SUBJECT[constants.ACCOUNT_CONFIRMATION],
            message=EMAIL_BODY[constants.ACCOUNT_CONFIRMATION].format(
                user_first_name=user.first_name,
                user_last_name=user.last_name,
            ),
        )
        return Response(
            {
                "detail": "User acccount has been confirmed successfully",
            },
            status.HTTP_200_OK,
        )


class PasswordResetEmailView(views.APIView):
    """
    Send an email to user if the email exists and user is_active
    """

    serializer_class = EmailSerializer
    permission_classes = [AllowAny]
    RESET_PASSWORD_EVENT = "RESET_PASSWORD"

    def post(self, request):
        """Accept email and send email to that user containing a unique signed token"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data.get("email"))
            if not user.is_active:
                return Response(
                    {
                        "detail": "User inactive, please activate your account before proceeding"
                    },
                    status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid email, not found"}, status.HTTP_404_NOT_FOUND
            )
        else:
            user.email_user(
                subject=EMAIL_SUBJECT[constants.RESET_PASSWORD],
                message=EMAIL_BODY[constants.RESET_PASSWORD].format(
                    user_first_name=user.first_name,
                    user_last_name=user.last_name,
                    secret_key_signed_code=signing.dumps(user.id),
                ),
            )
        return Response(
            {"detail": "An email with password reset code has been sent successfully."},
            status.HTTP_200_OK,
        )


class PasswordResetConfirmationView(views.APIView):
    """Checks whether the provided signed code sent on email is valid"""

    permission_classes = [AllowAny]

    def post(self, request, signed_user_token):
        """."""

        try:
            user_id = signing.loads(signed_user_token, max_age=timedelta(days=2))
            User.objects.get(id=user_id)
        except signing.SignatureExpired:
            return Response(
                {"detail": "Signature expired, please proceed to reset password again"},
                status.HTTP_400_BAD_REQUEST,
            )
        except signing.BadSignature:
            return Response(
                {"detail": "Invalid signature"}, status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status.HTTP_404_NOT_FOUND)
        return Response(
            {"detail": "Signature validation successful"}, status.HTTP_200_OK
        )


class PasswordResetChangeView(views.APIView):
    """."""

    permission_classes = [AllowAny]
    serializer_class = PasswordResetChangeSerializer

    def post(self, request, signed_user_token):
        """."""

        try:
            user_id = signing.loads(signed_user_token, max_age=timedelta(days=2))
            user = User.objects.get(id=user_id)
        except signing.SignatureExpired:
            return Response(
                {"detail": "Signature expired, please proceed to reset password again"},
                status.HTTP_400_BAD_REQUEST,
            )
        except signing.BadSignature:
            return Response(
                {"detail": "Invalid signature"}, status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data["password"])
            user.save()
        return Response({"detail": "Password reset successful"}, status.HTTP_200_OK)


class UserSearchView(generics.ListAPIView):
    """Search user objects either by email, first_name, last_name and their user_id"""

    permission_classes = [IsAccessAllowedToGroup]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filterset_class = UserFilterSet
