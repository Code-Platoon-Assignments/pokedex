from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from move_app.models import Move


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
