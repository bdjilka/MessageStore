from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from msgapp.models import Message, History, StoreUser

# Register your models here.


class StoreUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = StoreUser


class StoreUserAdmin(UserAdmin):
    form = StoreUserChangeForm


admin.site.register(StoreUser, UserAdmin)
admin.site.register(Message)
admin.site.register(History)
