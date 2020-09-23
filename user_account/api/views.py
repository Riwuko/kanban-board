from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user_account.api.serializers import RegistrationSerializer


@api_view(
    [
        "POST",
    ]
)
def registration_view(request):
    print(request.data)
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data["response"] = "New user registered."
        data["email"] = user.email
        data["username"] = user.username
    else:
        data["response"] = "User registration failed."
        data["errors"] = serializer.errors
    return Response(data)