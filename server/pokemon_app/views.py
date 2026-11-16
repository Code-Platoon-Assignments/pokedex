from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from move_app.serializers import PokemonMoveSerializer

from .models import Pokemon
from .serializers import PokemonSerializer


class AllPokemon(APIView):
    def get(self, request):
        pokemon = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemon, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APokemon(APIView):
    def get(self, request, id):
        pokemon = get_object_or_404(Pokemon, id=id)
        serializer = PokemonSerializer(pokemon)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        pokemon = get_object_or_404(Pokemon, id=id)
        serializer = PokemonSerializer(pokemon, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        pokemon = get_object_or_404(Pokemon, id=id)
        serializer = PokemonSerializer(pokemon, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APokemonMove(APIView):
    def get(self, request, poke_id, move_id):
        pokemon = get_object_or_404(Pokemon, id=poke_id)
        pokemon_move = get_object_or_404(pokemon.current_moves.all(), id=move_id)
        serializer = PokemonMoveSerializer(pokemon_move)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, poke_id, move_id):
        pokemon = get_object_or_404(Pokemon, id=poke_id)
        pokemon_move = get_object_or_404(pokemon.current_moves.all(), id=move_id)
        data = {**request.data, "pokemon": pokemon.id}
        serializer = PokemonMoveSerializer(pokemon_move, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, poke_id, move_id):
        pokemon = get_object_or_404(Pokemon, id=poke_id)
        pokemon_move = get_object_or_404(pokemon.current_moves.all(), id=move_id)
        data = {**request.data, "pokemon": pokemon.id}
        serializer = PokemonMoveSerializer(pokemon_move, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
