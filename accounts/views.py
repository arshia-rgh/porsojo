from rest_framework import generics

from accounts.serializer import UserRegistrationSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
