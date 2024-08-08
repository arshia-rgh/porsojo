import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ReportConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.content = self.scope["url_route"]["kwargs"]["content"]
        self.id = self.scope["url_route"]["kwargs"]["id"]

        self.content_group_name = f"{self.content}_{self.id}"

        await self.accept()
        await self.channel_layer.group_add(self.content_group_name, self.channel_name)

    async def disconnect(self, close_code):
        # Leave report group
        await self.channel_layer.group_discard(self.content_group_name, self.channel_name)

    async def on_view(self, event):
        await self.send(json.dumps({"type": "view", "views": event["views"]}))

    async def on_response_count(self, event):
        await self.send(json.dumps({"type": "response_count", "response_count": event["response_count"]}))

    async def on_response_add(self, event):
        await self.send(json.dumps({"type": "response_add", "response": event["response"]}))
