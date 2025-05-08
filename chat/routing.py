from django.urls import path
from chat.consumers import ChatComputerConsumer, ComputerConsumer, ChatFriendConsumer

websocket_urlpatterns = [
    path("ws/chat/computers/<str:name>/", ChatComputerConsumer.as_asgi()),
    path("ws/chat/friends/<str:username>/", ChatFriendConsumer.as_asgi()),
    path("ws/computer/", ComputerConsumer.as_asgi()),
]
