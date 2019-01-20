from rest_framework import serializers
from .models import Message, History, StoreUser
from djoser.serializers import UserCreateSerializer


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация пользователя """

    class Meta:
        model = StoreUser
        fields = ('id', 'username')


class UserRegistrationSerializer(UserCreateSerializer):
    """ Серилизация пользователя для авторизации """

    class Meta(UserCreateSerializer.Meta):
        model = StoreUser
        fields = ('username', 'password')


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
    user = UserSerializer()

    class Meta:
        model = History
        fields = ('message', 'text', 'date', 'user')
