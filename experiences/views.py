from rest_framework import generics
from .models import Perk
from .serializers import PerkSerializer


class PerkListCreateAPI(generics.ListCreateAPIView):
    serializer_class = PerkSerializer
    queryset = Perk.objects.all()


class PerkRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PerkSerializer
    queryset = Perk.objects.all()
