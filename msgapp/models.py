from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

# Create your models here.


class Message(models.Model):
    """ Модель сообщения пользователя """
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.CASCADE)
    publish_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)
    text = models.TextField(verbose_name='Текст сообщения', max_length=300)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def save(self, *args, **kwargs):
        """ Переопределение сохранения для добавления возможности ведения истории изменений """
        super(Message, self).save()
        History.objects.create(
            message=self,
            text=self.text,
        )


class History(models.Model):
    """ Модель истории изменения сообщений """
    message = models.ForeignKey(to=Message, verbose_name='Сообщение', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата изменения', auto_now_add=True)
    text = models.TextField(verbose_name='Текст', max_length=300)

    class Meta:
        verbose_name = 'История изменения'
        verbose_name_plural = 'История изменений'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)