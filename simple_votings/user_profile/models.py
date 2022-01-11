from django.db import models

from base import BaseModel


class Vote(BaseModel):
    theme = models.TextField()
    description = models.TextField()
    answer1 = models.TextField()
    answer2 = models.TextField()
    result = models.TextField()
