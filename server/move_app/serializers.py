from rest_framework import serializers
from .models import Move, PokemonMove


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ["id", "name", "description", "type", "power", "pp"]


class PokemonMoveSerializer(serializers.ModelSerializer):
    move = MoveSerializer(read_only=True)
    move_id = serializers.PrimaryKeyRelatedField(
        queryset=Move.objects.all(), source="move", write_only=True
    )

    class Meta:
        model = PokemonMove
        fields = ["id", "pokemon", "move", "move_id", "current_pp", "disabled"]
        extra_kwargs = {"pokemon": {"write_only": True}}

    def validate(self, attrs):
        move = attrs.get("move") or self.instance.move
        current_pp = attrs.get("current_pp", self.instance.current_pp if self.instance else None)
        if current_pp is not None and current_pp > move.pp:
            raise serializers.ValidationError(
                {"current_pp": f"{move.name} has a maximum of {move.pp} PP."}
            )
        return attrs
