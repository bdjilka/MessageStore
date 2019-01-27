# MessageStore
Система хранения сообщений пользователей с ведением истории

**Install python requirements**

> pip install -r requirements.txt

## Build Setup
1) Apply migrations

> python manage.py migrate

2) Create superuser with default login:password and start task on deleting old history

> python manage.py init

3) Start project

> python manage.py runserver

4) Start redis server

> redis-server

5) Init workers for celery

> celery -A msgstore worker --concurrency=4 --beat --scheduler django --loglevel=info -n worker


6) run front: message-store-vue

```
Build Setup of frontend

# serve with hot reload at localhost:8080 from directory .../msgstore-vue
npm run dev

# if not running, try:
sufo npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report


For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
```

## Documentation on API methods:
> localhost:8000/docs

## Tests
To run tests in root directory:
> ./manage.py test

To get tests coverage info:
Run:
> coverage html

Then open file htmlcov/index.html in browser
