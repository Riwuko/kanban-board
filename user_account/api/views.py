from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user_account.api.serializers import RegistrationSerializer


@api_view(["POST",])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data["response"] = "New user registered."
        data["email"] = user.email
    else:
        data["response"] = "User registration failed."
        data["errors"] = serializer.errors
    return Response(data)
