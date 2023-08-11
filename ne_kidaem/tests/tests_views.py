from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from blog.models import Post, Subscription


class PostViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        data = {"title": "Test Post", "text": "This is a test post."}
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_post(self):
        post = Post.objects.create(
            title="Test Post", text="This is a test post.", author=self.user
        )
        response = self.client.get(f"/api/posts/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Post")

    def test_update_post(self):
        post = Post.objects.create(
            title="Test Post", text="This is a test post.", author=self.user
        )
        data = {"title": "Updated Test Post"}
        response = self.client.patch(f"/api/posts/{post.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Test Post")

    def test_delete_post(self):
        post = Post.objects.create(
            title="Test Post", text="This is a test post.", author=self.user
        )
        response = self.client.delete(f"/api/posts/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=post.id).exists())


class UserFeedViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_subscribed_posts(self):
        subscribed_user = User.objects.create_user(
            username="subscribeduser", password="testpassword"
        )
        subscription = Subscription.objects.create(
            subscriber=self.user, author=subscribed_user
        )
        post = Post.objects.create(
            title="Subscribed Post",
            text="This is a subscribed post.",
            author=subscribed_user,
        )

        response = self.client.get("/api/user-feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Subscribed Post")
