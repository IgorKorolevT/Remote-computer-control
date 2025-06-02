from django.urls import path

from computer.web import views

# app_name = "api"

urlpatterns = [
    path("add/", views.add_pk, name="add"),
    path("<str:name>/detail/", views.ComputerDetailView.as_view(), name="detail"),
    path("", views.ComputerListView.as_view(), name="list"),
]
