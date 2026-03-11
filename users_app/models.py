from django.db import models
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
# 		fullname
# 		email
# 		(Login auf mail ändern)

# Create your models here.
class User(AbstractUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

 