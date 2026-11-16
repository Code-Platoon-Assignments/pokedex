from django.urls import path

from .views import AllPokemon

urlpatterns = [
    path('', AllPokemon.as_view(), name='all_pokemon'),
]
