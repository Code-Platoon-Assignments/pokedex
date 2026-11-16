from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from pokemon_app.models import Pokemon, PokemonType


class Move(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z][a-z]*([ -][A-Z][a-z]*)*$",
                message="Each word in a move name must start with a capital letter, followed by lowercase letters. Words are separated by a space or a hyphen.",
            )
        ],
    )
    type = models.CharField(
        max_length=20,
        choices=PokemonType.choices,
        default=PokemonType.NORMAL,
    )
    power = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(250)],
    )
    pp = models.PositiveIntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(40)],
    )
    description = models.TextField(
        default="Unknown",
        validators=[MinLengthValidator(7), MaxLengthValidator(150)],
    )

    def __str__(self):
        return f"{self.name} ({self.type}, {self.power} power, {self.pp} PP)"


class PokemonMove(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="current_moves")
    move = models.ForeignKey(Move, on_delete=models.CASCADE, related_name="learned_by")
    current_pp = models.PositiveIntegerField(blank=True)
    disabled = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["pokemon", "move"], name="unique_pokemon_move"),
        ]

    def __str__(self):
        return f"{self.pokemon.name} knows {self.move.name} ({self.current_pp}/{self.move.pp} PP)"

    def clean(self):
        if self.current_pp is not None and self.current_pp > self.move.pp:
            raise ValidationError(
                {"current_pp": f"{self.move.name} has a maximum of {self.move.pp} PP."}
            )

    def save(self, *args, **kwargs):
        if self.current_pp is None or self.current_pp > self.move.pp:
            self.current_pp = self.move.pp
        super().save(*args, **kwargs)
