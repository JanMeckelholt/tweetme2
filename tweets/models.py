import random
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    #id = models.AutoField(primary_key=true)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,100)
        }

    #def __str__(self):
    #    return self.content
