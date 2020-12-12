from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


login_urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="login_refresh"),
]

password_reset_urlpatterns = [
    path("", views.PasswordResetEmailView.as_view(), name="password_reset_email"),
    path(
        "confirm/<str:signed_user_token>/",
        views.PasswordResetConfirmationView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "change/<str:signed_user_token>/",
        views.PasswordResetChangeView.as_view(),
        name="password_reset_change",
    ),
]

urlpatterns = [
    path("", views.RegistrationView.as_view(), name="register"),
    path("search/", views.UserSearchView.as_view(), name="search"),
    path(
        "confirm/<str:signed_user_token>/",
        views.AccountConfirmationView.as_view(),
        name="account_confirmation",
    ),
    path(
        "resend-activation/",
        views.ResendActivationEmailView.as_view(),
        name="resend_activation_email",
    ),
    path("login/", include(login_urlpatterns)),
    path("password-reset/", include(password_reset_urlpatterns)),
]
