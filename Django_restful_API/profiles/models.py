import random
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    job = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default='profile_images/profile.png')
    location = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(null=False, blank=True, unique=False, db_index=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        slug_1 = slugify(self.user.id)
        slug_2 = str(random.randint(1000, 9999))
        self.slug = slug_1 + slug_2
        super().save(*args, **kwargs)