from django.urls import path
from .views import *
from .views import register, login
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", todo_list, name="todo_list"),

    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # For refreshing access token
    path("add/", add_todo, name="add_todo"),
    path("delete/<int:todo_id>/", delete_todo, name="delete_todo"),
    path("update/<int:todo_id>/", update_todo, name="update_todo"),
  
]
