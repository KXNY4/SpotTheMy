from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomerUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)