import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(default=uuid.uuid4, max_length=100, blank=True, unique=True)
    email = models.EmailField(unique=True)
    middle_name=models.CharField(max_length=50, blank=True,null=True)
    account_activated = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=["username"]