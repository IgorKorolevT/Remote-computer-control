from django.urls import path
from computer.api import views

app_name = "api"

urlpatterns = [
    path("", views.ComputerAPIView.as_view()),
]
