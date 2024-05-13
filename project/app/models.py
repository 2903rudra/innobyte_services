from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from .manager import *
# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.IntegerField(max_length=6,null=True,blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    