from django.urls import path

from computer.web import views

# app_name = "api"

urlpatterns = [
    path("add/", views.add_pk, name="add"),
]
