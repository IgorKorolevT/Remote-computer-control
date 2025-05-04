import json
from datetime import datetime
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Computer


def create_message(message, pk_name, timestamp):
    """Create message"""
    # TODO


class ChatComputerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            user.channel_name = self.channel_name
            await sync_to_async(user.save)()
            self.user = user
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        self.user.channel_name = None
        await sync_to_async(self.user.save)()

    async def receive(self, text_data: str):
        data = json.loads(text_data)
        message = data["message"]
        pk_name = data["receiver"]
        timestamp = data["date"]
        create_message(message, pk_name, timestamp)

        pk = await sync_to_async(Computer.objects.filter(name=pk_name).first)()
        if pk:
            context = {"message": message, "channel_user": self.scope["user"].channel_name,
                       "type": "pk_private_message"}
            await self.channel_layer.send(pk.channel_name, context)
        else:
            # TODO : Error
            pass

    async def user_private_message(self, event):
        message = event["message"]
        sender = event["sender"]
        # TODO: date
        time_send = str(datetime.now())
        data = json.dumps({"message": message, "sender": sender, "date": time_send})
        await self.send(text_data=data)


class ComputerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        headers = dict(self.scope["headers"])
        name, password = headers.get(b"name"), headers.get(b"password")
        if name and password:
            name, password = name.decode(), password.decode()
            pk = await sync_to_async(Computer.objects.filter(name=name, password=password).first)()
            if pk:
                pk.channel_name = self.channel_name
                await sync_to_async(pk.save)()
                self.pk = pk
                await self.accept()
                return
        await self.close()

    async def disconnect(self, close_code):
        self.pk.channel_name = None
        await sync_to_async(self.pk.save)()

    async def receive(self, text_data):
        data = json.loads(text_data)
        channel_user = data["channel_user"]
        context = {"message": data["message"], "sender": self.pk.nickname, "type": "user_private_message"}
        await self.channel_layer.send(channel_user, context)

    async def pk_private_message(self, event):
        message = event["message"]
        channel_user = event["channel_user"]
        data = json.dumps({"message": message, "channel_user": channel_user})
        await self.send(text_data=data)
