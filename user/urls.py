from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("profile/", views.UserDetailView.as_view(), name="profile"),
    path("update_user/", views.UserUpdateView.as_view(), name="update_user"),
    path("delete_user/", views.UserDeleteView.as_view(), name="delete_user"),
    path("", views.index, name="home"),
    path("add/computers/", views.add_pk, name="add_computer"),
]
