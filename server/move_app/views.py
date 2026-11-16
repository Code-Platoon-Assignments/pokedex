from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Move
from .serializers import MoveSerializer


class AllMoves(APIView):
    def get(self, request):
        moves = Move.objects.all()
        serializer = MoveSerializer(moves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
