from django.urls import path
from .views import Amenities, AmenityDetail, Rooms

urlpatterns = [
    path("", Rooms.as_view()),
    path("amenities/", Amenities.as_view()),
    path("amenities/<int:room_pk>/", AmenityDetail.as_view()),
]
