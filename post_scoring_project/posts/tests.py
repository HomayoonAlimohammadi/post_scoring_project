from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Post, Score

User = get_user_model()


class PostAPITestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

        # Create test posts
        self.post1 = Post.objects.create(title="Post 1", description="Description 1")
        self.post2 = Post.objects.create(title="Post 2", description="Description 2")

        # Create test scores
        self.score1_user1 = Score.objects.create(
            user=self.user1, post=self.post1, score=4
        )
        self.score2_user1 = Score.objects.create(
            user=self.user1, post=self.post2, score=3
        )
        self.score1_user2 = Score.objects.create(
            user=self.user2, post=self.post1, score=5
        )

    def test_list_posts_with_scores(self):
        client = APIClient()
        response = client.get(reverse("posts-view"))

        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the list of posts is in the response
        self.assertEqual(len(response.data), 2)

        # Check if the average score and number of scores are included for each post
        for post_data in response.data:
            post = Post.objects.get(pk=post_data["id"])
            self.assertIn("average_score", post_data)
            self.assertIn("num_scores", post_data)

    def test_score_post(self):
        client = APIClient()

        # Log in as user1
        client.login(username="user1", password="password1")

        # Score a post
        data = {"post": self.post1.id, "score": 2}
        response = client.post(reverse("scores-view"), data, format="json")

        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the score was updated
        updated_score = Score.objects.get(user=self.user1, post=self.post1)
        self.assertEqual(updated_score.score, 2)

        # Check if the post's average score was updated
        post1 = Post.objects.get(pk=self.post1.id)
        self.assertEqual(post1.calculate_average_score(), 3.5)
