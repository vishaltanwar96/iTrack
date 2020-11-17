from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationView, AccountConfirmationView


urlpatterns = [
    path("", RegistrationView.as_view(), name="register"),
    path(
        "confirm/<str:signed_user_token>/",
        AccountConfirmationView.as_view(),
        name="account_confirmation",
    ),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
]
