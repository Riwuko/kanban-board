from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from user_account.models.user_account import UserAccount


class UserAdmin(UserAdmin):
    model = UserAccount
    list_display = [
        "email",
    ]


admin.site.register(UserAccount, UserAdmin)
