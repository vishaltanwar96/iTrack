from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("tasks", views.TaskViewSet)

urlpatterns = []
urlpatterns += router.urls
