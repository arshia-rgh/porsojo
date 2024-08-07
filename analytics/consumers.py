import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ReportFormConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.form_id = self.scope["url_route"]["kwargs"]["form_id"]
        self.form_group_name = f"form_{self.form_id}"

        await self.accept()
        await self.channel_layer.group_add(self.form_group_name, self.channel_name)

    async def disconnect(self, close_code):
        # Leave report group
        await self.channel_layer.group_discard(self.form_group_name, self.channel_name)

    async def on_view(self, event):
        await self.send(json.dumps({"type": "view", "views": event["views"]}))

    async def on_response_count(self, event):
        await self.send(
            json.dumps(
                {"type": "response_count", "response_count": event["response_count"]}
            )
        )

    async def on_response_add(self, event):
        await self.send(
            json.dumps({"type": "response_add", "response": event["response"]})
        )


class ReportProcessConsumer(AsyncWebsocketConsumer):
    """
    AsyncWebsocketConsumer for process reports serving reports to active
    clients on the channel. It is connected to signals to :
    -   on_view : Real-time number of views.
    -   on_response_count : Real-time number of responses.
    -   on_response_add : Real-time update of responses.
    """

    async def connect(self):
        self.process_id = self.scope["url_route"]["kwargs"]["process_id"]
        self.process_group_name = f"process_{self.process_id}"

        await self.accept()
        await self.channel_layer.group_add(self.process_group_name, self.channel_name)

    async def disconnect(self, close_code):
        # Leave report group
        await self.channel_layer.group_discard(
            self.process_group_name, self.channel_name
        )

    async def on_view(self, event):
        await self.send(json.dumps({"type": "view", "views": event["views"]}))

    async def on_response_count(self, event):
        await self.send(
            json.dumps(
                {"type": "response_count", "response_count": event["response_count"]}
            )
        )

    async def on_response_add(self, event):
        await self.send(
            json.dumps({"type": "response_add", "response": event["response"]})
        )
