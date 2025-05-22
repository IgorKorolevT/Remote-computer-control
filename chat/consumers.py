import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Computer
from chat.utils import acreate_message, str_time
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
        try:
            pk = await sync_to_async(Computer.objects.get)(name=pk_name)
            if pk:
                await acreate_message(
                    text=message, sender=self.user, recipient=pk, timestamp=timestamp
                )
            if pk and pk.channel_name:
                context = {
                    "message": message,
                    "user_id": self.user.id,
                    "type": "pk_private_message",
                }
                await self.channel_layer.send(pk.channel_name, context)
        except Computer.DoesNotExist:
            pass  # TODO: send message that this computer doesn't exist

    async def user_private_message(self, event):
        sender = event["sender"]
        name_pk = self.scope["url_route"]['kwargs']['name']
        if sender == name_pk:
            message = event["message"]
            time_send = event["date"]
            data = json.dumps({"message": message, "sender": sender, "date": time_send})
            await self.send(text_data=data)


class ComputerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        headers = dict(self.scope["headers"])
        name, password = headers.get(b"name"), headers.get(b"password")
        if name and password:
            name, password = name.decode(), password.decode()
            try:
                pk = await sync_to_async(Computer.objects.get)(name=name)
                if not pk.check_password(password):
                    await self.close()
                self.pk = pk
                await self._set_channel_name(self.channel_name)
                await self.accept()
            except Computer.DoesNotExist:
                await self.close()

        else:
            await self.close(code=401)

    async def disconnect(self, close_code):
        await self._set_channel_name(None)

    async def receive(self, text_data: str = None, bytes_data=None):
        data = json.loads(text_data)
        user_id = data["user_id"]
        text = data["message"]

        try:
            user = await sync_to_async(User.objects.get)(pk=user_id)
        except User.DoesNotExist:
            pass  # TODO: send message that user id isn't correct
        else:
            ms = await acreate_message(text=text, sender=self.pk, recipient=user)
            if user.channel_name:
                context = {
                    "message": text,
                    "sender": self.pk.name,
                    "date": str_time(ms.timestamp),
                    "type": "user_private_message",
                }
                await self.channel_layer.send(user.channel_name, context)

    async def pk_private_message(self, event):
        message = event["message"]
        user_id = event["user_id"]
        data = json.dumps({"message": message, "user_id": user_id})
        await self.send(text_data=data)

    async def _set_channel_name(self, channel_name: None | str):
        self.pk.channel_name = channel_name
        await sync_to_async(self.pk.save)()
