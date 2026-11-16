from django.core.exceptions import ValidationError

from pokemon_app.models import Pokemon

Pokemon.objects.filter(name="snorlax").delete()

snorlax = Pokemon(name="snorlax", level=150, type="sleepy", description="Zzz")
try:
    snorlax.full_clean()
    snorlax.save()
except ValidationError as error:
    print(error.message_dict)
print(snorlax.id)

snorlax = Pokemon(
    name="Snorlax",
    level=30,
    type="normal",
    description="It eats nearly 900 pounds of food every day.",
)
try:
    snorlax.full_clean()
    snorlax.save()
except ValidationError as error:
    print(error.message_dict)
print(snorlax.id, snorlax)
