from django.contrib import admin
from .models import Move, PokemonMove
# Register your models here.
admin.site.register([Move, PokemonMove])
