from rest_framework import routers

from .views import TodoViewSet

router = routers.DefaultRouter()
router.register("", TodoViewSet)

urlpatterns = []

urlpatterns += router.urls
