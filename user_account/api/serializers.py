from rest_framework import serializers
from user_account.models.user import UserAccount


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["email", "username", "password"]

    def save(self):
        account = UserAccount(
            email=self.validated_data["email"], username=self.validated_data["username"]
        )
        password = self.validated_data["password"]
        account.set_password(password)
        account.save()
        return account
