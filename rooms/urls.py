from django.urls import path
from .views import (
    AmenityCreateListAPI,
    AmenityRetrieveUpdateDestroyAPI,
    RoomListCreateAPI,
    RoomDetail,
    RoomReviewListAPI,
    RoomPhotos,
)

urlpatterns = [
    path("", RoomListCreateAPI.as_view()),
    path("<int:pk>", RoomDetail.as_view()),
    path("<int:pk>/reviews", RoomReviewListAPI.as_view()),
    path("<int:pk>/photos", RoomPhotos.as_view()),
    path("amenities/", AmenityCreateListAPI.as_view()),
    path("amenities/<int:room_pk>/", AmenityRetrieveUpdateDestroyAPI.as_view()),
]
