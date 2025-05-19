from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path('', views.chat, name='chat'),
    path('computers/<str:name>', views.chat_computer, name='chat_computers'),
]
