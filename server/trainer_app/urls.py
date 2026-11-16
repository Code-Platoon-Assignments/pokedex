from django.urls import path

from .views import LogIn, LogOut, Me, Register

urlpatterns = [
    path('auth/register/', Register.as_view(), name='register'),
    path('auth/login/', LogIn.as_view(), name='login'),
    path('auth/logout/', LogOut.as_view(), name='logout'),
    path('users/me/', Me.as_view(), name='me'),
]
