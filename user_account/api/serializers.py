from rest_framework import serializers

from user_account.models.user_account import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["email", "password"]

    def save(self):
        account = UserAccount(
            email=self.validated_data["email"],
        )
        account.set_password(self.validated_data["password"])
        account.save()
        return account
