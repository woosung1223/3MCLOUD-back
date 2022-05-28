from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
     IdToken = models.TextField() # user pool token
    # user pool token은 이후에 credential으로 교환