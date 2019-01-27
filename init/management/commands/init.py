from __future__ import absolute_import, unicode_literals
from django.core.management.base import BaseCommand
from msgapp.models import StoreUser
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import os
import logging
import json
from msgstore_config.settings import TASK_PERIOD, DELTA


class Command(BaseCommand):
    help = 'Инициализация проекта для хранения сообщений и их истории изменений.'

    @staticmethod
    def _create_superuser():
        """
        Создание суперюзера
        """
        try:
            StoreUser.objects.get(is_superuser=True)
            logging.info('Суперюзер уже существуют')
        except StoreUser.DoesNotExist:
            login = os.getenv('SUPERUSER_NAME', 'admin')
            pswd = os.getenv('SUPERUSER_PSWD', 'password')
            StoreUser.objects.create_superuser(username=login, password=pswd, email='')
            logging.info('Создан суперюзер по стандартным параметрам окружения.')

    @staticmethod
    def _create_task():
        """
        Заведение задачи по удалению старых записей в истории сообщений
        """
        # TODO: Сделать проверку на сущестовование интервала и самой задачи
        # TASK_PERIOD = os.getenv('TASK_PERIOD', 30)
        # DELTA = os.getenv('DELTA', 30)

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=DELTA,
            period=IntervalSchedule.SECONDS,
        )

        PeriodicTask.objects.create(
            interval=schedule,
            name='History cleaner',  # simply describes this periodic task.
            task='msgapp.tasks.clear_old_history',  # name of task.
            args=json.dumps([TASK_PERIOD]),
        )

    def handle(self, *args, **options):
        self._create_superuser()
        self._create_task()
        print('Initialization finished.')
