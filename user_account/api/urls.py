from django.urls import path

from user_account.api.views import UserCreateView, UserDetailView, UserLoginView

app_name = "user_account"

urlpatterns = [
    path("register", UserCreateView.as_view(), name="register"),
    path("login", UserLoginView.as_view(), name="login"),
    path("user/<int:pk>", UserDetailView.as_view(), name="user_detail"),
]
