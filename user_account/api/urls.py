from django.urls import path
from user_account.api.views import (
    registration_view,
)

app_name = "user_account"

urlpatterns = [
    path("register", registration_view, name="register"),
]
