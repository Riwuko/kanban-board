from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from user_account.api.views import UserCreateView, UserDetailView

app_name = "user_account"

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("user/<int:pk>", UserDetailView.as_view(), name="user_detail"),
]
