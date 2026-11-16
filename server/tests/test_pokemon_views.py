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
from trainer_app.models import Trainer


class PokemonViewTests(APITestCase):
    fixtures = ["pokemon_data.json", "move_data.json", "pokemon_move_data.json"]

    def setUp(self):
        trainer = Trainer.objects.create_user("ash@pokedex.com", "pikachu123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {trainer.auth_token.key}")

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

    def test_post_a_pokemon(self):
        body = {
            "name": "Eevee",
            "level": 5,
            "type": "normal",
            "description": "It has an unstable genetic makeup.",
            "captured": True,
        }
        response = self.client.post(reverse("all_pokemon"), body, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Eevee")
        self.assertEqual(response.data["current_moves"], [])
        self.assertEqual(Pokemon.objects.count(), 6)
        self.assertTrue(Pokemon.objects.filter(id=response.data["id"], name="Eevee").exists())

    def test_post_with_invalid_data_returns_400(self):
        response = self.client.post(
            reverse("all_pokemon"), {"name": "eevee", "level": 500}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data), {"name", "level"})
        self.assertEqual(Pokemon.objects.count(), 5)

    def test_delete_a_pokemon(self):
        url = reverse("a_pokemon", kwargs={"id": 4})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertEqual(Pokemon.objects.count(), 4)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_unknown_pokemon_returns_404(self):
        response = self.client.delete(reverse("a_pokemon", kwargs={"id": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Pokemon.objects.count(), 5)


class PokemonMoveViewTests(APITestCase):
    fixtures = ["pokemon_data.json", "move_data.json", "pokemon_move_data.json"]

    def setUp(self):
        trainer = Trainer.objects.create_user("ash@pokedex.com", "pikachu123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {trainer.auth_token.key}")

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

    def test_post_a_pokemon_move(self):
        url = reverse("a_pokemon_moves", kwargs={"poke_id": 2})

        response = self.client.post(url, {"move_id": 3}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["move"]["name"], "Thunder Shock")
        self.assertEqual(response.data["current_pp"], 30)
        self.assertEqual(PokemonMove.objects.count(), 4)
        self.assertEqual(PokemonMove.objects.get(id=response.data["id"]).pokemon_id, 2)

    def test_post_pokemon_move_with_invalid_data_returns_400(self):
        url = reverse("a_pokemon_moves", kwargs={"poke_id": 1})

        response = self.client.post(url, {"move_id": 1}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(PokemonMove.objects.count(), 3)

    def test_delete_a_pokemon_move(self):
        url = reverse("a_pokemon_move", kwargs={"poke_id": 1, "move_id": 1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PokemonMove.objects.count(), 2)
        self.assertTrue(Move.objects.filter(id=1).exists())
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_unknown_pokemon_move_returns_404(self):
        url = reverse("a_pokemon_move", kwargs={"poke_id": 1, "move_id": 9999})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(PokemonMove.objects.count(), 3)
