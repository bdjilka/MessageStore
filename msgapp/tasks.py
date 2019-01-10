from __future__ import absolute_import
import datetime
import logging
from msgapp.models import History
from msgstore.celery import app


@app.task()
def clear_old_history(delta):
    """
    Очищение записей в истории сообщений старше delta
    :param delta: количество дней
    :return:
    """
    target_date = datetime.datetime.now() + datetime.timedelta(-delta)
    history_to_delete = History.objects.filter(date__lt=target_date)
    count = history_to_delete.count()
    history_to_delete.delete()
    logging.info("Task on history cleaning finished. Deleted '%s' messages." % count)
    return print("Task on history cleaning finished. Deleted '%s' messages." % count)
