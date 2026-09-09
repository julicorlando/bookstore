from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .api_views import CommentViewSet, FeedAPIView, FollowToggleAPIView, LikeToggleAPIView, MeAPIView, PostViewSet, RegisterAPIView

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="api_register"),
    path("login/", obtain_auth_token, name="api_login"),
    path("me/", MeAPIView.as_view(), name="api_me"),
    path("feed/", FeedAPIView.as_view(), name="api_feed"),
    path("users/<str:username>/follow/", FollowToggleAPIView.as_view(), name="api_follow"),
    path("posts/<int:post_id>/like/", LikeToggleAPIView.as_view(), name="api_like"),
    path("", include(router.urls)),
]
