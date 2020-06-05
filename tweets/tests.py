from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Tweet
# Create your tests here.
User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='abc', password='somepassword')
        self.user_b = User.objects.create_user(username='def', password='somepassword')
        Tweet.objects.create(content="first test content", user=self.user)
        Tweet.objects.create(content="second test content", user=self.user)
        Tweet.objects.create(content="third test content", user=self.user)
        Tweet.objects.create(content="fourth test content", user=self.user)
        Tweet.objects.create(content="fifth test content - userb", user=self.user_b)
        self.initalCount = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet = Tweet.objects.create(content="sixth test content", user=self.user)
        self.assertEqual(tweet.id, 6)
        self.assertEqual(tweet.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":1, "action":"like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":2, "action":"like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
        response = client.post("/api/tweets/action/", {"id":2, "action":"unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)

    def test_retweet_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":2, "action":"retweet"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.initalCount + 1, Tweet.objects.all().count())
        self.assertNotEqual(response.json().get("id"), 2)

    def test_tweet_create_api_view(self):
        data = {"content": "This is my test tweet for creat-view"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.initalCount + 1, response.json().get("id"))

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("content"), "first test content")
        self.assertEqual(response.json().get("id"), 1)

    def test_tweet_delete_api_view(self):
        self.initalCount
        client = self.get_client()
        response = client.delete("/api/tweets/3/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.initalCount -1, Tweet.objects.all().count())
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.initalCount -2, Tweet.objects.all().count())
        response = client.delete("/api/tweets/1/delete/") #already deleted
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.initalCount -2, Tweet.objects.all().count())
        response = client.delete("/api/tweets/5/delete/") #different user
        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.initalCount -2, Tweet.objects.all().count())
