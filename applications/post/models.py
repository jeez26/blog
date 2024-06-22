from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    title = models.CharField(max_length=128)


class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=256)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=256)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    likes = models.SmallIntegerField(default=0)
    views = models.SmallIntegerField(default=0)
    comments = models.ManyToManyField(to=Comment)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(to=Tag)
