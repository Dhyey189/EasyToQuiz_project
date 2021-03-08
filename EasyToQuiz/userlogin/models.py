from django.db import models
from django.contrib.auth.models import User, auth

# Create your models here.
class user_signup(models.Model):
    username = models.CharField(max_length=20)
    emailid = models.CharField(max_length=40)
    password = models.CharField(max_length=20)

class quiz_data(models.Model):
    quiztitle = models.CharField(max_length=40)
    # quizid = models.CharField(max_length=40)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)

class Question_data(models.Model):
    quizid = models.ForeignKey("quiz_data",on_delete=models.CASCADE)
    qtitle = models.CharField(max_length=500)
    qtype = models.BooleanField(default=False)

class option_data(models.Model):
    questionid = models.ForeignKey("Question_data",on_delete=models.CASCADE)
    # quizid = models.ForeignKey(Question_data)
    option = models.CharField(max_length=500)

