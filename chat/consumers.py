import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class WSChatView(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'post_for_room_' + str(self.scope['url_route']['kwargs']['id'])
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(
            self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        )

    def receive(self, **kwargs):
        data = json.loads(kwargs['text_data'])
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                **data
            }
        )
