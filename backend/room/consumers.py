import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Room
from django.contrib.auth.models import User



class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # return await super().connect()


    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


        # return await super().disconnect(code)
    
    async def receive(self, text_data):

        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message,
                'username' : username,
                'room' : room,
            }
        )

        # return await super().receive(text_data, bytes_data)

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        await self.send(text_data=json.dumps({
                'message' : message,
                'username' : username,
                'room' : room,
        }))

    
    @sync_to_async
    def save_message(self, _username, _room, message):
        
        user = User.objects.get(username=_username)
        room = Room.objects.get(slug=_room)

        Message.objects.create(users=user, room=room, content=message)