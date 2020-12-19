from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, ProjectRemarksHistoryViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("remarks", ProjectRemarksHistoryViewSet)

urlpatterns = []
urlpatterns += router.urls
