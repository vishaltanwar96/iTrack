from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer


class UserRegistrationView(CreateAPIView):
    """."""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """."""

        user = super(UserRegistrationView, self).perform_create(serializer)
        # THIS EMAIL MUST BE REPLACED WITH A CELERY TASK AND EMAIL MESSAGE WITH A HTML MESSAGE TEMPLATE
        user.email_user(
            "[ITRACK] ACCOUNT HAS BEEN CREATED",
            f"Greetings! {user.first_name.title()} {user.last_name.title()}\n\n Your iTrack user account has been created, Please follow the link below to verfiy/confirm your account",
        )
