from django.db import models

from base import BaseModel


class UserVote(BaseModel): # голос пользователя
    description = models.TextField()
    answer1 = models.TextField()
    answer2 = models.TextField()
    result = models.TextField()


class Vote(BaseModel): # голосование
    theme = models.TextField()
    description = models.TextField()
    answers = models.TextField()
