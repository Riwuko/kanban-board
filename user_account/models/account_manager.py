from django.contrib.auth.models import BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email: 
            raise ValueError("Email can't be empty")

        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
