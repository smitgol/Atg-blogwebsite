from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse


# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='Blog_pics')
    mode_choices = (
        ('Private', 'Private'),
        ('Public', 'Public'),
    )
    post_mode = models.CharField(max_length=9, choices=mode_choices)

    def get_absolute_url(self):
        return reverse('home')