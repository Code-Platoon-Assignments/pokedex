from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from move_app.models import Move
from tests.answers import TEST_GET_A_MOVE_ANSWER


class MoveViewTests(APITestCase):
    fixtures = ["move_data.json"]

    def test_get_all_moves(self):
        response = self.client.get(reverse("all_moves"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.data), Move.objects.count())

        names = [move["name"] for move in response.data]
        self.assertIn("Thunderbolt", names)
        self.assertIn("Quick Attack", names)

        for move in response.data:
            self.assertEqual(
                list(move),
                ["id", "name", "description", "type", "power", "pp"],
            )

    def test_get_a_move(self):
        response = self.client.get(reverse("a_move", kwargs={"id": 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            TEST_GET_A_MOVE_ANSWER
        )

    def test_unknown_move_returns_404(self):
        response = self.client.get(reverse("a_move", kwargs={"id": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_post_a_move(self):
        body = {
            "name": "Tackle",
            "type": "normal",
            "power": 40,
            "pp": 35,
            "description": "A full-body charge attack.",
        }
        response = self.client.post(reverse("all_moves"), body, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Tackle")
        self.assertEqual(Move.objects.count(), 4)
        self.assertTrue(Move.objects.filter(id=response.data["id"], name="Tackle").exists())

    def test_post_move_with_invalid_data_returns_400(self):
        response = self.client.post(reverse("all_moves"), {"name": "Tackle"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("pp", response.data)
        self.assertEqual(Move.objects.count(), 3)

    def test_delete_a_move(self):
        url = reverse("a_move", kwargs={"id": 3})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Move.objects.count(), 2)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_unknown_move_returns_404(self):
        response = self.client.delete(reverse("a_move", kwargs={"id": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Move.objects.count(), 3)
