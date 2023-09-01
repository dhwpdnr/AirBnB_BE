from django.urls import path
from .views import PerkListCreateAPI, PerkRetrieveUpdateDestroyAPI

urlpatterns = [
    path("perks/", PerkListCreateAPI.as_view()),
    path("perks/<int:pk>/", PerkRetrieveUpdateDestroyAPI.as_view()),
]
