from django.contrib import admin
from .models import Room, Messages


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Messages)
class MessageAdmin(admin.ModelAdmin):
    pass
