import jwt
from django.conf import settings
from rest_framework import exceptions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user_account.api.serializers import UserAccountSerializer
from user_account.models.user_account import UserAccount


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data["email"], status=status.HTTP_200_OK)
