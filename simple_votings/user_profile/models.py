from django.contrib.auth import get_user_model
from django.db import models

from base import BaseModel


class Vote(BaseModel):  # голосование
    theme = models.TextField()
    description = models.TextField()
    answers = models.TextField()


class UserVote(BaseModel): # голос пользователя
    vote_id = models.TextField()
    results = models.TextField()
    user_id = models.TextField()


class Report(BaseModel):
    author = models.ForeignKey(get_user_model(), models.CASCADE)
    theme = models.TextField()
    content = models.TextField()
    vote = models.ForeignKey(Vote, models.CASCADE)
