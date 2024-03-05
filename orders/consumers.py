import json

from channels.generic.websocket import AsyncWebsocketConsumer


class OrderConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.order_id = None

    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        await self.channel_layer.group_add(
            self.order_id, self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.order_id, self.channel_name
        )

    async def send_notification(self, event: dict):
        print(event)
        await self.send(text_data=json.dumps(event))
