from django.db import models
import uuid
from datetime import datetime
from django.utils.text import slugify
from categories.models import Category


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images', default="post_images/content.png")
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    content = models.TextField(blank=True)
    slug = models.SlugField(null=False, blank=True, unique=False, db_index=True)
    categories = models.ManyToManyField(Category, related_name="post")

    def __str__(self):
        return self.caption

    def save(self, *args, **kwargs):
        self.slug = slugify(self.caption)
        super().save(*args, **kwargs)


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username