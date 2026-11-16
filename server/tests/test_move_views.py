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
