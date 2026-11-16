from rest_framework import serializers
from move_app.serializers import PokemonMoveSerializer
from .models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    current_moves = PokemonMoveSerializer(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = ["id", "name", "level", "type", "description", "captured", "date_encountered", "current_moves"]
