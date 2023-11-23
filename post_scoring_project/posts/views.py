from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from posts.models import Post, Score
from posts.serializers import PostSerializer, ScoreSerializer, UserSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ScoreCreate(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_class = [IsAuthenticatedOrReadOnly()]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post")
        score_value = request.data.get("score")
        user = request.user

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            score = Score.objects.get(user=user, post=post)
        except Score.DoesNotExist:
            score = Score.objects.create(
                user=user,
                post=post,
                score=score_value,
            )

        # Update the score value
        score.score = score_value
        score.save()

        data = self.serializer_class(score).data

        return Response(data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
