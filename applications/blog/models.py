from django.db import models
from django.contrib.auth.models import User

from applications.post.models import Post


class Blog(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='blog_owner')
    authors = models.ManyToManyField(to=User, related_name='blog_authors')
    posts = models.ManyToManyField(to=Post, related_name='blog_post')
    subscribers = models.ManyToManyField(to=User, related_name='blog_subscribers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

