from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "user"

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("profile/", views.profile, name="profile"),
    path("", views.index, name="home"),
    path("add/computers/", views.add_pk, name="add_computer"),
]
