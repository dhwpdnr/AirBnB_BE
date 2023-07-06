from django.contrib import admin
from .models import ChattingRoom, Messages


@admin.register(ChattingRoom)
class ChattingRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Messages)
class MessageAdmin(admin.ModelAdmin):
    pass
