import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            print(user)
            print(self.scope["url_route"]["kwargs"]["name"])
            await self.accept()
        await self.close()

    async def disconnect(self, close_code):
        print(close_code)

    async def receive(self, text_data: str):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        # username = text_data_json["username"]
        # await self.channel_layer.group_send(
        #     self.roomGroupName, {
        #         "type": "sendMessage",
        #         "message": message,
        #         "username": username,
        #     })
        if text_data == 'heartbeat':
            await self.send(text_data='heartbeat_ack')
        else:
            await self.send(text_data="Привіт, WebSocket!")

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))
