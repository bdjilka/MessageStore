from rest_framework import serializers
from .models import Message, History
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация пользователя """

    class Meta:
        model = User
        fields = ('id', 'username')


class MessageSerializer(serializers.ModelSerializer):
    """ Сериализация сообщений """
    author = UserSerializer()

    class Meta:
        model = Message
        fields = ('id', 'author', 'publish_date', 'last_modify', 'text')


class MessagePostSerializer(serializers.ModelSerializer):
    """ Сериализация для создания сообщений """

    class Meta:
        model = Message
        fields = ('text',)


class HistorySerializer(serializers.ModelSerializer):
    """ Сериализация истории """

    class Meta:
        model = History
        fields = ('message', 'text', 'date')
