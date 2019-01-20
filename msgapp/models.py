from django.db import models
from django.contrib.auth.models import AbstractUser


class StoreUser(AbstractUser):
    """ Модель пользователя """
    pass


class Message(models.Model):
    """ Модель сообщения пользователя """
    author = models.ForeignKey(to=StoreUser, verbose_name='Автор', on_delete=models.CASCADE)
    publish_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)
    text = models.TextField(verbose_name='Текст сообщения', max_length=300)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class History(models.Model):
    """ Модель истории изменения сообщений """
    message = models.ForeignKey(to=Message, verbose_name='Сообщение', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата изменения', auto_now_add=True)
    text = models.TextField(verbose_name='Текст', max_length=300)
    user = models.ForeignKey(to=StoreUser, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'История изменения'
        verbose_name_plural = 'История изменений'