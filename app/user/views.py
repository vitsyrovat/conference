# from rest_framework import viewsets
from rest_framework import generics
from user.serializers import UserSerializer


class UserCreate(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = UserSerializer
