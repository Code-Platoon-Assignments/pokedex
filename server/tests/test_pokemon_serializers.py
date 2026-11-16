from datetime import date

from django.test import TestCase

from pokemon_app.models import Pokemon
from pokemon_app.serializers import PokemonSerializer
from tests.answers import (
    TEST_SERIALIZING_EVERY_POKEMON,
    TEST_SERIALIZING_ONE_POKEMON_ANSWER,
)


class PokemonSerializerTests(TestCase):

    def test_valid_data_creates_a_pokemon(self):
        data = {
            "name": "Eevee",
            "level": 25,
            "type": "normal",
            "description": "Its genetic code is unstable, so it can evolve in many ways.",
        }
        serializer = PokemonSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        eevee = serializer.save()
        self.assertIsInstance(eevee, Pokemon)
        self.assertEqual(eevee.name, "Eevee")
        self.assertEqual(Pokemon.objects.count(), 1)

    def test_missing_fields_use_model_defaults(self):
        serializer = PokemonSerializer(data={"name": "Ditto"})
        self.assertTrue(serializer.is_valid())
        ditto = serializer.save()
        self.assertEqual(ditto.level, 1)
        self.assertEqual(ditto.type, "normal")
        self.assertEqual(ditto.description, "Unknown")

    def test_invalid_data_is_rejected(self):
        data = {"name": "eevee", "level": 150, "type": "fairy", "description": "Cute"}
        serializer = PokemonSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {"name", "level", "type", "description"})
        self.assertEqual(Pokemon.objects.count(), 0)

    def test_save_before_is_valid_raises_an_error(self):
        serializer = PokemonSerializer(data={"name": "Eevee"})
        with self.assertRaises(AssertionError):
            serializer.save()

    def test_serializing_one_pokemon(self):
        pikachu = Pokemon.objects.create(
            name="Pikachu",
            level=12,
            type="electric",
            description="It stores electricity in the electric sacs on its cheeks.",
            date_encountered=date(2026, 2, 14),
        )
        serializer = PokemonSerializer(pikachu)
        self.assertEqual(
            serializer.data,
            {
                "id": pikachu.id,
                "name": "Pikachu",
                "level": 12,
                "type": "electric",
                "description": "It stores electricity in the electric sacs on its cheeks.",
                "captured": False,
                "date_encountered": "2026-02-14",
                "current_moves": [],
            },
        )

    def test_serializing_many_pokemon(self):
        Pokemon.objects.create(name="Pikachu")
        Pokemon.objects.create(name="Bulbasaur")
        serializer = PokemonSerializer(Pokemon.objects.all(), many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEqual(len(serializer.data), 2)
        self.assertCountEqual([pokemon["name"] for pokemon in serializer.data], ["Pikachu", "Bulbasaur"])

    def test_serializing_many_without_many_true_fails(self):
        Pokemon.objects.create(name="Pikachu")
        serializer = PokemonSerializer(Pokemon.objects.all())
        with self.assertRaises(AttributeError):
            serializer.data

    def test_full_update_replaces_fields(self):
        pikachu = Pokemon.objects.create(name="Pikachu", level=12, type="electric")
        data = {
            "name": "Raichu",
            "level": 30,
            "type": "electric",
            "description": "Its long tail serves as a ground to protect itself from its own high voltage.",
            "captured": True,
            "date_encountered": "2026-02-14",
        }
        serializer = PokemonSerializer(pikachu, data=data)
        self.assertTrue(serializer.is_valid())
        raichu = serializer.save()
        self.assertEqual(raichu.id, pikachu.id)
        self.assertEqual(raichu.name, "Raichu")
        self.assertEqual(Pokemon.objects.count(), 1)

    def test_update_without_partial_requires_required_fields(self):
        pikachu = Pokemon.objects.create(name="Pikachu", level=12, type="electric")
        serializer = PokemonSerializer(pikachu, data={"level": 13})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_partial_update_changes_only_the_fields_sent(self):
        pikachu = Pokemon.objects.create(name="Pikachu", level=12, type="electric")
        serializer = PokemonSerializer(pikachu, data={"level": 13}, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        pikachu.refresh_from_db()
        self.assertEqual(pikachu.level, 13)
        self.assertEqual(pikachu.name, "Pikachu")
        self.assertEqual(pikachu.type, "electric")

    def test_partial_update_still_runs_validators(self):
        pikachu = Pokemon.objects.create(name="Pikachu", level=12, type="electric")
        serializer = PokemonSerializer(pikachu, data={"level": 150}, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("level", serializer.errors)


class PokemonFixtureTests(TestCase):
    fixtures = ["pokemon_data.json", "move_data.json", "pokemon_move_data.json"]

    def test_fixture_loads_every_pokemon(self):
        self.assertEqual(Pokemon.objects.count(), 5)

    def test_serializing_one_pokemon_from_the_fixture(self):
        pikachu = Pokemon.objects.get(name="Pikachu")
        serializer = PokemonSerializer(pikachu)
        self.assertEqual(serializer.data, TEST_SERIALIZING_ONE_POKEMON_ANSWER)

    def test_serializing_every_pokemon_from_the_fixture(self):
        serializer = PokemonSerializer(Pokemon.objects.all(), many=True)
        self.assertEqual(len(serializer.data), 5)
        self.assertCountEqual(
            [pokemon["name"] for pokemon in serializer.data],
            TEST_SERIALIZING_EVERY_POKEMON,
        )
        for pokemon in serializer.data:
            self.assertEqual(
                list(pokemon),
                ["id", "name", "level", "type", "description", "captured", "date_encountered", "current_moves"],
            )
