from django.urls import path

from .views import AllPokemon, APokemon, APokemonMove, APokemonMoves

urlpatterns = [
    path('', AllPokemon.as_view(), name='all_pokemon'),
    path('<int:id>/', APokemon.as_view(), name='a_pokemon'),
    path('<int:poke_id>/moves/', APokemonMoves.as_view(), name='a_pokemon_moves'),
    path('<int:poke_id>/moves/<int:move_id>/', APokemonMove.as_view(), name='a_pokemon_move'),
]
