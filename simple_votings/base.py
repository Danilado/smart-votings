from django.db import models


class BaseModel(models.Model):
    """
    Базовый класс модели. Нужен для того чтобы Pycharm не ругался на наличие менеджера в модели.

    Также см. https://stackoverflow.com/a/56845199
    """
    objects = models.Manager()

    class Meta:
        abstract = True
