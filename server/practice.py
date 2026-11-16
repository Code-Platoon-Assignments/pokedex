from pokemon_app.models import Pokemon

pikachu = Pokemon.objects.get(name="Pikachu")
pikachu.level_up()
pikachu.change_caught_status()
print(pikachu)

mew = Pokemon.objects.create(name="Mew")
print(mew.id, mew)
print(Pokemon.objects.all())
