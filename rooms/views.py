from rest_framework.views import APIView
from django.db import transaction
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from reviews.seriralizers import ReviewSerializer
from medias.serializers import PhotoSerializer


class AmenityCreateListAPI(generics.ListCreateAPIView):
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()


class AmenityRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()


class RoomListCreateAPI(generics.ListCreateAPIView):
    serializer_class = RoomListSerializer
    queryset = Room.objects.all()
    detail_serializer = RoomDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.detail_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @transaction.atomic()
    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_id = request.data.get("category")
                if not category_id:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_id)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                        raise ParseError("The Category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                try:
                    room = serializer.save(owner=request.user, category=category)
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity Not Found.")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    @transaction.atomic()
    def put(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated
        serializer = RoomDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category_id = request.data.get("category")
        if not category_id:
            raise ParseError("Category is required.")
        try:
            category = Category.objects.get(pk=category_id)
            if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                raise ParseError("The Category kind should be rooms")
        except Category.DoesNotExist:
            raise ParseError("Category not found")
        amenity_list = []
        amenities_pk = request.data.get("amenities")
        for amenities in amenities_pk:
            try:
                amenity = Amenity.objects.get(pk=amenities)
                if not amenity:
                    raise ParseError("amenities가 알맞지 않습니다.")
                amenity_list.append(amenity)
            except Amenity.DoesNotExist:
                pass
        update_room = serializer.save(
            category=category,
            amenities=amenity_list,
        )
        return Response(RoomDetailSerializer(update_room).data)


def delete(self, request, pk):
    room = self.get_object(pk)
    if not request.user.is_authenticated:
        raise NotAuthenticated
    if room.owner != request.user:
        raise PermissionDenied
    room.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# 전체 api 리팩토링 필요
class RoomReviewListAPI(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self, pk):
        try:
            queryset = self.queryset.get(id=pk)
        except Room.DoesNotExist:
            raise NotFound
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        reviews = queryset.reviews.all()
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)


class RoomPhotos(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
