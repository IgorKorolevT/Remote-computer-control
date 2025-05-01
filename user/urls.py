from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "user"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register_new_user, name="register"),
    path("profile/<int:pk>/", views.UserDetailView.as_view(), name="profile"),
    path("", views.index, name="home"),
]
