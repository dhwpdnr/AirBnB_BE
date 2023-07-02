from django.contrib import admin
from .models import Experiences, Perk


@admin.register(Experiences)
class ExperiencesAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "start", "end")


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = ("name", "detail", "explanation")
