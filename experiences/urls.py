from django.urls import path
from .views import PerkListCreateAPI, PerkDetail

urlpatterns = [
    path("perks/", PerkListCreateAPI.as_view()),
    path("perks/<int:pk>/", PerkDetail.as_view()),
]
