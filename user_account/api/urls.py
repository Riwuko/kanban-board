from django.urls import path

from user_account.api.views import UserCreateView

app_name = "user_account"

urlpatterns = [
    path("register", UserCreateView.as_view(), name="register"),
]
