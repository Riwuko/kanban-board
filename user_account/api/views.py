from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user_account.models.user import UserAccount
from user_account.api.serializers import RegistrationSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = UserAccount.objects.all()
