from datetime import date

from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models


class PokemonType(models.TextChoices):
    NORMAL = "normal", "Normal"
    FIRE = "fire", "Fire"
    WATER = "water", "Water"
    ELECTRIC = "electric", "Electric"
    GRASS = "grass", "Grass"
    ICE = "ice", "Ice"
    FIGHTING = "fighting", "Fighting"
    POISON = "poison", "Poison"
    GROUND = "ground", "Ground"
    FLYING = "flying", "Flying"
    PSYCHIC = "psychic", "Psychic"
    BUG = "bug", "Bug"
    ROCK = "rock", "Rock"
    GHOST = "ghost", "Ghost"
    DRAGON = "dragon", "Dragon"


class Pokemon(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z][a-z.']*( [A-Z][a-z.']*)*$",
                message="Each word in a name must start with a capital letter, followed by lowercase letters, periods, or apostrophes.",
            )
        ],
    )
    level = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    type = models.CharField(
        max_length=20,
        choices=PokemonType.choices,
        default=PokemonType.NORMAL,
    )
    description = models.TextField(
        default="Unknown",
        validators=[MinLengthValidator(7), MaxLengthValidator(150)],
    )
    captured = models.BooleanField(default=False)
    date_encountered = models.DateField(default=date.today)

    def __str__(self):
        status = "captured" if self.captured else "not captured"
        return f"{self.name} (Lv. {self.level}) - {status}"

    def level_up(self):
        self.level += 1
        self.save()

    def change_caught_status(self):
        self.captured = not self.captured
        self.save()
