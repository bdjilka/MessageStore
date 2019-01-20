from django_filters import rest_framework
from .models import Message


class MessageFilter(rest_framework.FilterSet):
    """ Фильтрации сообщений по неполному совпадению """
    username = rest_framework.CharFilter(field_name="author__username", lookup_expr="contains")
    text = rest_framework.CharFilter(field_name="text", lookup_expr="contains")
    publish_date = rest_framework.DateTimeFilter(field_name="publish_date", lookup_expr="contains")
    last_modify = rest_framework.DateTimeFilter(field_name="last_modify", lookup_expr="contains")

    class Meta:
        model = Message
        fields = ['username', 'text', 'publish_date', 'last_modify']
