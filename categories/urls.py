from django.urls import path
from .views import categories, category

urlpatterns = [path("", categories), path("<int:pk>/", category)]
