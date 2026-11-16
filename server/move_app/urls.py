from django.urls import path

from .views import AllMoves

urlpatterns = [
    path('', AllMoves.as_view(), name='all_moves'),
]
