from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

app_name = "user_account"

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
