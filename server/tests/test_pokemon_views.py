from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from move_app.models import Move, PokemonMove
from pokemon_app.models import Pokemon
from tests.answers import (
    TEST_GET_A_POKEMON_MOVE_ANSWER,
    TEST_SERIALIZING_EVERY_POKEMON,
    TEST_SERIALIZING_ONE_POKEMON_ANSWER,
)


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

    def test_get_a_pokemon(self):
        response = self.client.get(reverse("a_pokemon", kwargs={"id": 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            TEST_SERIALIZING_ONE_POKEMON_ANSWER
        )

    def test_unknown_pokemon_returns_404(self):
        response = self.client.get(reverse("a_pokemon", kwargs={"id": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_non_integer_id_returns_404(self):
        response = self.client.get("/api/v1/pokemon/pikachu/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # NOTE: Ideally we would test success and failure (400 and 404) for every update
    # method on every view (APokemon, AMove, and APokemonMove), but time constraints
    # for this lecture will not allow this. We test APokemon's patch method here.
    def test_patch_a_pokemon(self):
        url = reverse("a_pokemon", kwargs={"id": 3})
        before = self.client.get(url).data

        response = self.client.patch(url, {"level": 37, "captured": True}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {**before, "level": 37, "captured": True})
        self.assertEqual(response.data["name"], "Charizard")

    def test_patch_with_invalid_data_returns_400(self):
        response = self.client.patch(
            reverse("a_pokemon", kwargs={"id": 3}), {"level": 500}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("level", response.data)
        self.assertEqual(Pokemon.objects.get(id=3).level, 36)

    def test_patch_unknown_pokemon_returns_404(self):
        response = self.client.patch(
            reverse("a_pokemon", kwargs={"id": 9999}), {"level": 37}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PokemonMoveViewTests(APITestCase):
    fixtures = ["pokemon_data.json", "move_data.json", "pokemon_move_data.json"]

    def test_get_a_pokemon_move(self):
        url = reverse("a_pokemon_move", kwargs={"poke_id": 1, "move_id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            TEST_GET_A_POKEMON_MOVE_ANSWER
        )

    def test_unknown_pokemon_or_move_returns_404(self):
        urls = {
            "unknown pokemon": reverse("a_pokemon_move", kwargs={"poke_id": 9999, "move_id": 1}),
            "unknown move": reverse("a_pokemon_move", kwargs={"poke_id": 1, "move_id": 9999}),
        }
        for description, url in urls.items():
            with self.subTest(description):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_move_of_another_pokemon_returns_404(self):
        bulbasaur = Pokemon.objects.get(name="Bulbasaur")
        tackle = Move.objects.create(
            name="Tackle", type="normal", power=40, pp=35, description="A full-body charge attack."
        )
        bulbasaur_tackle = PokemonMove.objects.create(pokemon=bulbasaur, move=tackle)

        url = reverse(
            "a_pokemon_move",
            kwargs={"poke_id": 1, "move_id": bulbasaur_tackle.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
