from django.db import models

# Create your models here.

class User(models.Model):
    UserId = models.CharField(max_length=100)
    IdToken = models.TextField() # user pool token
    # user pool token은 이후에 credential으로 교환
