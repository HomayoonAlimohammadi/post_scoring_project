from django.contrib.auth.models import User
from rest_framework import serializers
from posts.models import Post, Score


class PostSerializer(serializers.ModelSerializer):
    average_score = serializers.SerializerMethodField()
    num_scores = serializers.SerializerMethodField()
    user_score = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_average_score(self, obj):
        return obj.calculate_average_score()

    def get_num_scores(self, obj):
        return obj.score_set.count()

    def get_user_score(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.get_user_score(user)
        return None


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")
