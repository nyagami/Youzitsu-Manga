
# from channels.db import database_sync_to_async
from channels.consumer import get_channel_layer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync

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
        self.channel_layer.group_send(
            self.group,
            {'type': 'notify', 'notifcation': notifcation}
        )

    async def notify(self, event, close=False):
        await self.send_json(event)

    # content must be decoded json
    @classmethod
    async def notify_all(self, content, usernames):
        for username in usernames:
            await get_channel_layer().group_send(
                username,
                {'type': 'notify', 'notification': content}
            )

    @classmethod
    async def notify_one(self, content, username):
        await get_channel_layer().group_send(
            username,
            {'type': 'notify', 'notification': content}
        )


class CommentConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # group should be like ^[a-z]_[\w_-]+
        self.group = self.scope['url_route']['kwargs']['article']
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
        await self.channel_layer.group_send(
            self.group,
            {'type': 'comment', 'comment': comment}
        )

    async def comment(self, event):
        await self.send_json(event)

    @classmethod
    def send_comment(self, article, content):
        async_to_sync(get_channel_layer().group_send)(
            article,
            {'type': 'comment', 'comment': content}
        )