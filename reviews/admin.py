from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by word!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [("good", "Good"), ("greate", "Greate"), ("awesome", "Awesome")]

    def queryset(self, request, queryset):
        word = self.value()
        if word:
            return queryset.filter(payload__contins=word)
        return queryset


class ScoreFilter(admin.SimpleListFilter):
    title = "Filter by Score!"
    parameter_name = "score"

    def lookups(self, request, model_admin):
        return [("bad", "Bad"), ("good", "Good")]

    def queryset(self, request, reviews):
        score = self.value()
        if score == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews.filter(rating__gte=3)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        ScoreFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
