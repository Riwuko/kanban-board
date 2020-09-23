import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import exceptions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_jwt.serializers import jwt_payload_handler
from user_account.api.serializers import UserAccountSerializer
from user_account.models.user_account import UserAccount


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()
    permission_classes = [AllowAny]


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed("username and password required")

        user = UserAccount.objects.get(email=email)
        if (user is None) or (not user.check_password(password)):
            raise exceptions.AuthenticationFailed("Wrong email or password")

        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        user_details = {}
        user_details["email"] = user.email
        user_details["token"] = token
        return Response(user_details, status=status.HTTP_200_OK)


