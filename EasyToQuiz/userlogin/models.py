from django.db import models

# Create your models here.
class user_signup(models.Model):
    username = models.CharField(max_length=20)
    emailid = models.CharField(max_length=40)
    password = models.CharField(max_length=20)