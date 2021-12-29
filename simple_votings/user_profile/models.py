from django.db import models

# Create your models here.

class Vote(models.Model):
    theme = models.TextField()
    description = models.TextField()
    answer1 = models.TextField()
    answer2 = models.TextField()
    result = models.TextField()

class Votes(models.Model):
    theme = models.TextField()
    description = models.TextField()
    answer1 = models.TextField()
    answer2 = models.TextField()

