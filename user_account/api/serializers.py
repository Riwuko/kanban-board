from rest_framework import serializers

from user_account.models.user import UserAccount


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["email", "password"]

    def save(self):
        account = UserAccount(
            email=self.validated_data["email"],
            password = self.validated_data["password"]
        )
        account.save()
        return account
