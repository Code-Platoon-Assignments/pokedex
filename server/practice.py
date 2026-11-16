from pokemon_app.models import Pokemon
from pokemon_app.serializers import PokemonSerializer

pikachu = Pokemon.objects.get(name="Pikachu")
print(PokemonSerializer(pikachu).data)
