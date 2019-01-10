from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
# , filters
from .models import Message, History
from django.contrib.auth.models import User
from .serializers import MessageSerializer, HistorySerializer, UserSerializer, MessagePostSerializer
import logging


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра списка пользователей
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint работы с сообщениями (добавление - просмотр - ведение истории - изменение - удаление)
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # filter_backends = (filters.SearchFilters, )
    # search_fields = ('text', 'publish_date', 'last_modify', 'author__username')

    def create(self, request, *args, **kwargs):
        """
        Создание сообщения
        Требуется только текст, дата создания заполняются сами, дата последнего изменения приравнивается к текущей
        Автор сообщения берется из данных реквеста
        Данная операция разрешена только автору сообщения или суперюзеру
        :param request: post-запрос, содержит информацию об авторизированном пользователе и текст сообщенич
        :param args:
        :param kwargs:
        :return: статус ответа 201 в случае успеха, 400/404 в случае неудачи
        """
        try:
            message = MessagePostSerializer(data=request.data)
            if message.is_valid():
                message.save(author=request.user)
                logging.info("New message added")
                return Response(status=201)
            else:
                return Response(status=400)
        except:
            return Response(status=404)

    def update(self, request, pk, *args, **kwargs):
        """
        Обновление сообщения
        Требуется только текст, дата изменения заполняется автоматически
        Данная операция разрешена только автору сообщения или суперюзеру
        :param request: put-запрос, содержит информацию о пользователе и текст сообщения
        :param pk: идентификатор сообщения
        :param args:
        :param kwargs:
        :return: статус ответа 201 в случае успеха, 400 в случае неудачи, 403 если у пользователя нет прав
        """
        try:
            user_id = request.user.id
            is_admin = request.user.is_superuser
            message = Message.objects.get(pk=pk)
            if message.author_id == user_id or is_admin:
                message.text = request.data['text']
                message.save()
                logging.info("Message updated")
                return Response(status=200)
            else:
                return Response(status=403)
        except:
            return Response(status=400)

    def destroy(self, request, pk, *args, **kwargs):
        """
        Удаление сообщения
        Данная операция разрешена только автору сообщения или суперюзеру
        :param request: delete-запрос, содержащий информацию о пользователе
        :param pk: идентификатор сообщения
        :param args:
        :param kwargs:
        :return: статус ответа 201 в случае успеха, 400 в случае неудачи, 403 если у пользователя нет прав
        """
        try:
            user_id = request.user.id
            is_admin = request.user.is_superuser
            message = Message.objects.get(pk=pk)
            if message.author_id == user_id or is_admin:
                message.delete()
                logging.info("Message deleted")
                return Response(status=200)
            else:
                return Response(status=403)
        except:
            return Response(status=400)

    @action(detail=True, methods=['get'])
    def history(self, request, pk):
        """
        Просмотр истории изменений сообщений
        :param request: get-запрос
        :param pk: идентификатор сообщения
        :return: сериализованный ответ с историей и статусом 201 вслучае успеха, 400 в случае неудачи
        """
        try:
            hist = History.objects.all().filter(message=pk)
            serializer = HistorySerializer(hist, many=True)
            return Response(data=serializer.data, status=201)
        except:
            return Response(status=400)


class HistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра истории всех сообщений[-ия]
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = History.objects.all()
    serializer_class = HistorySerializer
