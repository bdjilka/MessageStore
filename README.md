# MessageStore
Система хранения сообщений пользователей с ведением истории

**Install python requirements**

pip install -r requirements.txt

## Build Setup
1) Apply migrations

python manage.py migrate

2) Create superuser with default login:password and start task on deleting old history

python manage.py init

3) Start project

python manage.py runserver

4) Start redis server

redis-server

5) Init workers for celery

celery -A msgstore worker --concurrency=4 --beat --scheduler django --loglevel=info -n worker

## Documentation on API methods:
- localhost:8000/docs