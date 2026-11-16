from django.urls import path

from .views import AllMoves, AMove

urlpatterns = [
    path('', AllMoves.as_view(), name='all_moves'),
    path('<int:id>/', AMove.as_view(), name='a_move'),
]
