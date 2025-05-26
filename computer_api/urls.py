from django.urls import path
from . import views

app_name = "pk_api"

urlpatterns = [
    path("", views.ComputerAPIView.as_view()),
]
