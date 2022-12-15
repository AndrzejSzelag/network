from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


"""
IntegerField:               values from -2147483648 to 2147483647
PositiveSmallIntegerField:  values from 0 to 32767
PositiveIntegerField:       values from 0 to 2147483647
PositiveBigIntegerField:    values from 0 to 9223372036854775807
"""


class Post(models.Model):
    username = models.CharField(max_length=50)
    content = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }


class Follow(models.Model):
    username = models.CharField(max_length=50)
    follower = models.CharField(max_length=50)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.username,
            "follower": self.follower
        }


class Like(models.Model):
    postid = models.IntegerField()
    likedby = models.CharField(max_length=50)
    likes = models.PositiveIntegerField()

    def serialize(self):
        return {
            "id": self.postid,
            "likedby": self.likedby,
            "likes": self.likes
        }
