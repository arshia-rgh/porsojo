import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from surveys.models import Form, Process, Response


class ReportFormConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.form_id = self.scope["url_route"]["kwargs"]["form_id"]
        self.form_group_name = f"form_{self.form_id}"
        
        await self.accept()
        await self.channel_layer.group_add(
            self.form_group_name, self.channel_name)
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.form_group_name, self.channel_name
        )

    #async def receive(self, data):
    #    data["type"]

    async def on_view(self, event):
        await self.send(json.dumps({
            "type": "view",
            "views": event['views']}))
        
    async def on_response_count(self, event):
        await self.send(json.dumps({
            "type": "response_count",
            "response_count": event['response_count']}))
        
    async def on_response_add(self, event):
        await self.send(json.dumps({
            "type": "response_add",
            "response": event['response']}))
        
        



class ReportProcessConsumer(AsyncWebsocketConsumer):
    pass