from django.urls import path
from . import views

app_name = "event"
urlpatterns = [
    path("<str:name>", views.block, name="block"),
]
