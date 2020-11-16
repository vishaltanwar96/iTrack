from django.urls import path

from .views import UserRegistrationView, UserAccountConfirmationView


urlpatterns = [
    path("", UserRegistrationView.as_view()),
    path("confirm/<str:signed_user_token>/", UserAccountConfirmationView.as_view()),
]
