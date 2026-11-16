from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pokemon_app.models import Pokemon
from tests.answers import TEST_SERIALIZING_EVERY_POKEMON


class PokemonViewTests(APITestCase):
    fixtures = ["pokemon_data.json", "move_data.json", "pokemon_move_data.json"]

    def test_get_all_pokemon(self):
        response = self.client.get(reverse("all_pokemon"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.data), Pokemon.objects.count())
        self.assertCountEqual(
            [pokemon["name"] for pokemon in response.data],
            TEST_SERIALIZING_EVERY_POKEMON,
        )

        for pokemon in response.data:
            self.assertEqual(
                list(pokemon),
                ["id", "name", "level", "type", "description", "captured", "date_encountered", "current_moves"],
            )
