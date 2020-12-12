from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegistrationView,
    AccountConfirmationView,
    PasswordResetEmailView,
    PasswordResetConfirmationView,
    PasswordResetChangeView,
    ResendActivationEmailView,
    UserSearchView,
)


login_urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="login_refresh"),
]

password_reset_urlpatterns = [
    path("", PasswordResetEmailView.as_view(), name="password_reset_email"),
    path(
        "confirm/<str:signed_user_token>/",
        PasswordResetConfirmationView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "change/<str:signed_user_token>/",
        PasswordResetChangeView.as_view(),
        name="password_reset_change",
    ),
]

urlpatterns = [
    path("", RegistrationView.as_view(), name="register"),
    path("search/", UserSearchView.as_view(), name="search"),
    path(
        "confirm/<str:signed_user_token>/",
        AccountConfirmationView.as_view(),
        name="account_confirmation",
    ),
    path(
        "resend-activation/",
        ResendActivationEmailView.as_view(),
        name="resend_activation_email",
    ),
    path("login/", include(login_urlpatterns)),
    path("password-reset/", include(password_reset_urlpatterns)),
]
