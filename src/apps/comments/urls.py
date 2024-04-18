from rest_framework.routers import DefaultRouter

from .views import CommentViewSet

router = DefaultRouter()
router.register(r"recipe/(?P<slug>[^/.]+)/comments", CommentViewSet, basename="comment")

urlpatterns = router.urls
