import json
from channels.generic.websocket import AsyncWebsocketConsumer


class WSChatView(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'post_for_room_' + str(self.scope['url_route']['kwargs']['id'])
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                **json.loads(text_data)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            **event
        }))
