from django.contrib import admin

# Register your models here.
from api.telebot.models import TeleSettings

admin.site.register(TeleSettings)
