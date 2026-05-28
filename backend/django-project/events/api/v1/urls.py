from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, EventViewSet

router = SimpleRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("events", EventViewSet, basename="event")

urlpatterns = router.urls
