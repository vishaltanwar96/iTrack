from django.urls import path, include

from . import views

urlpatterns = [
    path("status/", views.StatusView.as_view(), name="status"),
    path("criticality/", views.CriticalityView.as_view(), name="criticality"),
    path("group/", views.GroupView.as_view(), name="group"),
]
