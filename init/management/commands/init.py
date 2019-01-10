from __future__ import absolute_import, unicode_literals
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework.authtoken.models import Token
import os
import logging
import json


class Command(BaseCommand):
    help = 'Инициализация проекта для хранения сообщений и их истории изменений.'

    @staticmethod
    def _create_superuser():
        """
        Создание суперюзера
        """
        try:
            User.objects.get(is_superuser=True)
            logging.info('Суперюзер уже существуют')
        except User.DoesNotExist:
            login = os.getenv('SUPERUSER_NAME', 'admin')
            pswd = os.getenv('SUPERUSER_PSWD', 'password')
            User.objects.create_superuser(username=login, password=pswd, email='')
            logging.info('Создан суперюзер по стандартным параметрам окружения.')

    @staticmethod
    def _create_task():
        """
        Заведение задачи по удалению старых записей в истории сообщений
        """
        # TODO: Сделать проверку на сущестовование интервала и самой задачи
        TASK_PERIOD = os.getenv('TASK_PERIOD', 30)
        DELTA = os.getenv('DELTA', 30)

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=TASK_PERIOD,
            period=IntervalSchedule.SECONDS,
        )

        PeriodicTask.objects.create(
            interval=schedule,
            name='History cleaner',  # simply describes this periodic task.
            task='msgapp.tasks.clear_old_history',  # name of task.
            args=json.dumps([DELTA]),
        )

        # app.conf.beat_schedule = {
        #     'old-history-clean': {
        #         'task': 'msgapp.tasks.clear_old_history',
        #         'schedule': TASK_PERIOD * 24 * 60 * 60,  # time in seconds
        #         'args': (DELTA,)  # maximum time to store history in days
        #     },
        # }

    @staticmethod
    def _create_tokens():
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)

    def handle(self, *args, **options):
        self._create_superuser()
        self._create_task()
        print('Initialization finished.')
