import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Computer
from chat.utils import acreate_message
from user.models import User


class SenderTypes: # TODO replace to more suitable place
    USER = "user"
    COMPUTER = "computer"



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            self.user = user
            await self._set_channel_name(self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self._set_channel_name()

    async def _set_channel_name(self, channel_name: str = None) -> None:
        self.user.channel_name = channel_name
        await sync_to_async(self.user.save)()


class ChatComputerConsumer(ChatConsumer):
    async def receive(self, text_data: str = None, bytes_data=None):
        data = json.loads(text_data)

        message = data["message"]
        pk_name = data["receiver"]
        try:
            pk = await sync_to_async(Computer.objects.get)(name=pk_name)
            ms = await acreate_message(
                text=message, sender=self.user, recipient=pk
            )
            base_context = {
                "message": ms.text,
                "sender": self.user.id,
                "date": ms.get_timestamp,
            }
            user_context = {**base_context,
                            "type_sender": SenderTypes.USER,
                            "type": "user_private_message"}
            await self.channel_layer.send(self.user.channel_name, user_context)
            if pk.channel_name:
                pk_context = {**base_context,
                              "type_sender": SenderTypes.COMPUTER,
                              "type": "pk_private_message"}
                await self.channel_layer.send(pk.channel_name, pk_context)
        except Computer.DoesNotExist:
            pass  # TODO: send message that this computer doesn't exist

    async def user_private_message(self, event):
        sender = event["sender"]
        message = event["message"]
        time_send = event["date"]
        data = {"message": message, "date": time_send}

        if event["type_sender"] == SenderTypes.USER and self.user.id == sender:
            data["sender"] = "You"
        elif event["type_sender"] == SenderTypes.COMPUTER and self.scope["url_route"]['kwargs']['name'] == sender:
            data["sender"] = sender
        else:
            raise TypeError("Type sender must be either user or computer")

        jdata = json.dumps(data)
        await self.send(text_data=jdata)


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
        await self._set_channel_name()

    async def receive(self, text_data: str = None, bytes_data=None):
        data = json.loads(text_data)
        user_id = data["receiver"]
        text = data["message"]

        try:
            user = await sync_to_async(User.objects.get)(pk=user_id)
            ms = await acreate_message(text=text, sender=self.pk, recipient=user)
            if user.channel_name:
                context = {
                    "message": ms.text,
                    "sender": self.pk.name,
                    "date": ms.get_timestamp,
                    "type_sender": SenderTypes.COMPUTER,
                    "type": "user_private_message",
                }
                await self.channel_layer.send(user.channel_name, context)
        except User.DoesNotExist:
            pass  # TODO: send message that user id isn't correct

    async def pk_private_message(self, event):
        event["type"] = "base"
        data = json.dumps(event)
        await self.send(text_data=data)

    async def _set_channel_name(self, channel_name: str = None) -> None:
        self.pk.channel_name = channel_name
        await sync_to_async(self.pk.save)()
