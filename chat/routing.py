from django.urls import path , include
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path("" , ChatConsumer.as_asgi()),
    path("ws/chat/computers/<str:name>/", ChatConsumer.as_asgi()),
]