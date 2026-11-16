from django.shortcuts import get_object_or_404
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


class AMove(APIView):
    def get(self, request, id):
        move = get_object_or_404(Move, id=id)
        serializer = MoveSerializer(move)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        move = get_object_or_404(Move, id=id)
        serializer = MoveSerializer(move, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        move = get_object_or_404(Move, id=id)
        serializer = MoveSerializer(move, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
