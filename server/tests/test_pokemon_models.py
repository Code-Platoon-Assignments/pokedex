from django.core.exceptions import ValidationError
from django.test import TestCase

from pokemon_app.models import Pokemon


class PokemonModelTests(TestCase):

    def build_pokemon(self, **overrides):
        data = {
            "name": "Pikachu",
            "level": 12,
            "type": "electric",
            "description": "It stores electricity in the electric sacs on its cheeks.",
        }
        data.update(overrides)
        return Pokemon(**data)

    def test_valid_pokemon_is_saved(self):
        pikachu = self.build_pokemon()
        pikachu.full_clean()
        pikachu.save()
        self.assertEqual(Pokemon.objects.count(), 1)
        self.assertEqual(Pokemon.objects.get(name="Pikachu").level, 12)

    def test_missing_fields_use_defaults(self):
        mew = Pokemon(name="Mew")
        mew.full_clean()
        self.assertEqual(mew.level, 1)
        self.assertEqual(mew.type, "normal")
        self.assertEqual(mew.description, "Unknown")
        self.assertFalse(mew.captured)

    def test_name_is_required(self):
        pokemon = self.build_pokemon(name="")
        with self.assertRaises(ValidationError) as error:
            pokemon.full_clean()
        self.assertIn("name", error.exception.message_dict)

    def test_name_longer_than_50_characters_fails(self):
        pokemon = self.build_pokemon(name="P" + "a" * 50)
        with self.assertRaises(ValidationError) as error:
            pokemon.full_clean()
        self.assertIn("name", error.exception.message_dict)

    def test_duplicate_name_fails(self):
        self.build_pokemon().save()
        duplicate = self.build_pokemon()
        with self.assertRaises(ValidationError) as error:
            duplicate.full_clean()
        self.assertIn("name", error.exception.message_dict)

    def test_negative_level_fails(self):
        pokemon = self.build_pokemon(level=-1)
        with self.assertRaises(ValidationError) as error:
            pokemon.full_clean()
        self.assertIn("level", error.exception.message_dict)

    def test_level_above_100_fails(self):
        pokemon = self.build_pokemon(level=150)
        with self.assertRaises(ValidationError) as error:
            pokemon.full_clean()
        self.assertIn("level", error.exception.message_dict)

    def test_level_zero_fails(self):
        pokemon = self.build_pokemon(level=0)
        with self.assertRaises(ValidationError) as error:
            pokemon.full_clean()
        self.assertIn("level", error.exception.message_dict)

    def test_improperly_formatted_names_fail(self):
        bad_names = ["pikachu", "PIKACHU", "Pika chu", "Ch4rizard", "Pikachu!"]
        for name in bad_names:
            with self.subTest(name=name):
                pokemon = self.build_pokemon(name=name)
                with self.assertRaises(ValidationError) as error:
                    pokemon.full_clean()
                self.assertIn("name", error.exception.message_dict)

    def test_names_with_spaces_periods_and_apostrophes_pass(self):
        good_names = ["Mr. Mime", "Farfetch'd"]
        for name in good_names:
            with self.subTest(name=name):
                pokemon = self.build_pokemon(name=name)
                pokemon.full_clean()

    def test_description_shorter_than_7_characters_fails(self):
        pokemon = self.build_pokemon(description="Cute")
        with self.assertRaises(ValidationError) as error:
            pokemon.full_clean()
        self.assertIn("description", error.exception.message_dict)

    def test_description_longer_than_150_characters_fails(self):
        pokemon = self.build_pokemon(description="a" * 151)
        with self.assertRaises(ValidationError) as error:
            pokemon.full_clean()
        self.assertIn("description", error.exception.message_dict)

    def test_type_outside_gen_1_fails(self):
        bad_types = ["fairy", "steel", "dark", "electricity"]
        for pokemon_type in bad_types:
            with self.subTest(type=pokemon_type):
                pokemon = self.build_pokemon(type=pokemon_type)
                with self.assertRaises(ValidationError) as error:
                    pokemon.full_clean()
                self.assertIn("type", error.exception.message_dict)
