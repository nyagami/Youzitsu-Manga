
# from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotifcationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group = self.scope['url_route']['kwargs']['username']
        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        notifcation = content['notification']
        notifcation


class CommentConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group = self.scope['url_route']['kwargs']['type'] + '_' + self.scope['url_route']['kwargs']['article']
        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        comment = content['comment']
        comment
