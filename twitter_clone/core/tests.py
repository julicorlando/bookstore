from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Follow, Like, Post

User = get_user_model()


class SocialNetworkTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="SenhaForte123!")
        self.bob = User.objects.create_user(username="bob", password="SenhaForte123!")
        self.carla = User.objects.create_user(username="carla", password="SenhaForte123!")

    def test_profile_created_automatically(self):
        self.assertEqual(self.alice.profile.user, self.alice)

    def test_feed_contains_only_followed_users_posts(self):
        Follow.objects.create(follower=self.alice, following=self.bob)
        bob_post = Post.objects.create(author=self.bob, content="Post do Bob")
        Post.objects.create(author=self.carla, content="Post da Carla")
        self.client.login(username="alice", password="SenhaForte123!")
        response = self.client.get(reverse("feed"))
        self.assertContains(response, bob_post.content)
        self.assertNotContains(response, "Post da Carla")

    def test_like_is_unique_per_user_and_post(self):
        post = Post.objects.create(author=self.bob, content="Teste")
        Like.objects.create(user=self.alice, post=post)
        self.assertEqual(post.likes.count(), 1)

    def test_user_cannot_follow_self_through_view(self):
        self.client.login(username="alice", password="SenhaForte123!")
        self.client.post(reverse("follow_toggle", args=["alice"]))
        self.assertFalse(Follow.objects.filter(follower=self.alice, following=self.alice).exists())
