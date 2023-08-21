from django.urls import path
from .views import (
    AmenityCreateListAPI,
    AmenityRetrieveUpdateDestroyAPI,
    Rooms,
    RoomDetail,
    RoomReviews,
    RoomPhotos,
)

urlpatterns = [
    path("", Rooms.as_view()),
    path("<int:pk>", RoomDetail.as_view()),
    path("<int:pk>/reviews", RoomReviews.as_view()),
    path("<int:pk>/photos", RoomPhotos.as_view()),
    path("amenities/", AmenityCreateListAPI.as_view()),
    path("amenities/<int:room_pk>/", AmenityRetrieveUpdateDestroyAPI.as_view()),
]
