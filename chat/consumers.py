import json
from datetime import datetime
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Computer
from chat.utils import acreate_message
from user.models import User


class ChatConsumer(AsyncWebsocketConsumer):
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


class ChatComputerConsumer(ChatConsumer):
    async def receive(self, text_data: str = None, bytes_data=None):
        data = json.loads(text_data)

        message = data["message"]
        pk_name = data["receiver"]
        timestamp = data["date"]
        pk = await sync_to_async(Computer.objects.filter(name=pk_name).first)()
        if pk:
            await acreate_message(text=message, sender=self.user, recipient=pk, timestamp=timestamp)
        if pk and pk.channel_name:
            context = {"message": message, "user_id": self.user.id,
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
            pk = await sync_to_async(Computer.objects.filter(name=name).first)()
            if pk is None:
                await self.close()  # TODO: code close connection
            if pk.check_password(password) is False:
                await self.close()  # TODO: code close connection
            await self._set_channel_name(self.channel_name)
            self.pk = pk
            await self.accept()
        else:
            await self.close() # TODO: code close connection

    async def disconnect(self, close_code):
        await self._set_channel_name(None)

    async def receive(self, text_data: str = None, bytes_data=None):
        data = json.loads(text_data)
        user_id = data["user_id"]
        text = data["message"]

        try:
            user = await sync_to_async(User.objects.get)(pk=user_id)
        except Exception as e:  # TODO: replace to more suitable Error DoesNotExist
            print(e)
        else:
            message = await acreate_message(text=text, sender=self.pk, recipient=user, timestamp=data.get("date"))
            if user.channel_name:
                context = {"message": text, "sender": self.pk.nickname, "type": "user_private_message"}
                await self.channel_layer.send(user.channel_name, context)

    async def pk_private_message(self, event):
        message = event["message"]
        user_id = event["user_id"]
        data = json.dumps({"message": message, "user_id": user_id})
        await self.send(text_data=data)

    async def _set_channel_name(self, channel_name: None | str):
        self.pk.channel_name = channel_name
        await sync_to_async(self.pk.save)()
