from django.db import models

# Create your models here.

class Votings(models.Model):
    title = models.CharField('Название', max_length=50)
    voted_yes = models.IntegerField('ЗА', default=0)
    voted_no = models.IntegerField('ПРОТИВ', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосования'
