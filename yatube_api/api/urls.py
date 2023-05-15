from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"groups", GroupViewSet, basename="group")
router.register(
    r"posts/(?P<post_id>\d+)/comments",
    CommentViewSet, basename="comments"
)
router.register("follow", FollowViewSet, basename="follow")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("auth/", include('djoser.urls')),
    path("auth/", include('djoser.urls.jwt')),
]
