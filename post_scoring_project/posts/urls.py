from django.urls import path

from posts.views import PostList, ScoreCreate, UserViewSet

urlpatterns = [
    path("posts/", PostList.as_view(), name="posts-view"),
    path("scores/", ScoreCreate.as_view(), name="scores-view"),
]
