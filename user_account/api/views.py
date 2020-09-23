from rest_framework import exceptions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user_account.api.serializers import RegistrationSerializer
from user_account.api.utils import generate_access_token, generate_refresh_token
from user_account.models.user import UserAccount


class UserCreateView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = UserAccount.objects.all()
    permission_classes = [AllowAny]


class UserLoginView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
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

        serialized_user = self.serializer_class(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = Response()
        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
        response.data = {
            "access_token": access_token,
            "user": serialized_user,
        }
        return response
