from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pokemon
from .serializers import PokemonSerializer


class AllPokemon(APIView):
    def get(self, request):
        pokemon = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemon, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
