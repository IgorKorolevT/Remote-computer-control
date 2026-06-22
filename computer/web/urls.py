from django.urls import path

from computer.web import views
# app_name = "api"

urlpatterns = [
    path("add/", views.add_pk, name="add"),
    path("<str:name>/detail/", views.ComputerDetailView.as_view(), name="detail"),
    path("<str:name>/update/", views.ComputerUpdateView.as_view(), name="update"),
    path("<str:name>/delete/", views.ComputerDeleteView.as_view(), name="delete"),
    path("<str:name>/toggle/", views.toggle_computer, name="toggle"),
    path("", views.ComputerListView.as_view(), name="list"),
]
