from rest_framework.views import APIView
from django.db import transaction
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
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
