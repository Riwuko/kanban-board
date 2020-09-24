from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from user_account.account_manager import AccountManager


class UserAccount(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    objects = AccountManager()

    def __str__(self):
        return self.email
