from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def calculate_average_score(self):
        total_scores = self.score_set.aggregate(total=models.Sum("score"))["total"]
        if total_scores is not None:
            num_scores = self.score_set.count()
            return total_scores / num_scores
        return 0  # Return 0 if there are no scores for the post

    def get_user_score(self, user):
        try:
            return self.score_set.get(user=user).score
        except Score.DoesNotExist:
            return None


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(choices=[(i, i) for i in range(6)])

    class Meta:
        unique_together = ("user", "post")
