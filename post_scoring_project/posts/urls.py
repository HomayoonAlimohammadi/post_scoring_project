from django.urls import path, include

from rest_framework.routers import DefaultRouter

from posts.views import PostList, ScoreCreate, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("posts/", PostList.as_view(), name="posts-view"),
    path("scores/", ScoreCreate.as_view(), name="scores-view"),
]
