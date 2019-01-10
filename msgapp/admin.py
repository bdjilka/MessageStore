from django.contrib import admin
from msgapp.models import Message, History

# Register your models here.

admin.site.register(Message)
admin.site.register(History)