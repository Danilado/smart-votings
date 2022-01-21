from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

from base import BaseModel


class Vote(BaseModel):  # голосование
    theme = models.TextField()
    description = models.TextField()
    answers = models.TextField()


class UserVote(BaseModel): # голос пользователя
    vote=models.ForeignKey(to=Vote, on_delete=models.CASCADE)
    results = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Report(BaseModel):
    author = models.ForeignKey(get_user_model(), models.CASCADE)
    theme = models.TextField()
    content = models.TextField()
