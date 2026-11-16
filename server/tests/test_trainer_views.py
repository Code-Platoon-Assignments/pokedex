from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from trainer_app.models import Trainer


class TrainerViewTests(APITestCase):
    def setUp(self):
        self.trainer = Trainer.objects.create_user("ash@pokedex.com", "pikachu123")
        self.token = self.trainer.auth_token.key

    def test_register(self):
        response = self.client.post(
            reverse("register"),
            {"email": "misty@pokedex.com", "password": "starmie123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(list(response.data), ["id", "email", "token"])
        misty = Trainer.objects.get(email="misty@pokedex.com")
        self.assertEqual(response.data["token"], misty.auth_token.key)
        self.assertTrue(misty.check_password("starmie123"))

    def test_register_with_a_taken_email(self):
        response = self.client.post(
            reverse("register"),
            {"email": "ash@pokedex.com", "password": "starmie123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Trainer.objects.count(), 1)

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {"email": "ash@pokedex.com", "password": "pikachu123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"token": self.token})

    def test_login_with_a_wrong_password(self):
        response = self.client.post(
            reverse("login"),
            {"email": "ash@pokedex.com", "password": "wrong"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("token", response.data)

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(key=self.token).exists())
        # the deleted token no longer authenticates
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_without_a_token(self):
        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Token.objects.filter(key=self.token).exists())

    def test_get_me(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        response = self.client.get(reverse("me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"id": self.trainer.id, "email": "ash@pokedex.com", "token": self.token},
        )

    def test_get_me_without_a_token(self):
        response = self.client.get(reverse("me"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_me(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        response = self.client.patch(
            reverse("me"),
            {"email": "ash.ketchum@pokedex.com", "password": "raichu12345"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "ash.ketchum@pokedex.com")
        self.trainer.refresh_from_db()
        self.assertTrue(self.trainer.check_password("raichu12345"))
