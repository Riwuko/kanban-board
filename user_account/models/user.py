from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from user_account.models.account_manager import AccountManager


class UserAccount(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    objects = AccountManager()

    def __str__(self):
        return self.email
