from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
<<<<<<< HEAD
from channels.db import database_sync_to_async
=======
from django.utils import timezone
>>>>>>> 0f43918c955c6ab9792a15248e764a6d9f4fe27c
import json
from .models import *
import sys
from chat.utils import * 
from django.template.loader import render_to_string




User = get_user_model()

class ChatConsumer(WebsocketConsumer):
   
    def fetch_messages(self, data):
        group=ChatGroup.objects.get(id=self.room_name)
        messages = Message.last_10_messages(group)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
    
    def get_group_receiver(self,obj):
        users=User.objects.filter(groups__name=obj.name)
        user = self.scope['user']
        
        if user.username == users[0].username:
            sender=users[0]
            receiver=users[1]
        else:
            sender=users[1]
            receiver=users[0]
        return receiver

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        chatgroup=ChatGroup.objects.get(id=self.room_name)
        if data['message']:
            message = Message.objects.create(
            author=author_user, 
            content=data['message'],chatgroup=chatgroup)
        else:
            message = Message()
            message.author=author_user
            message.chatgroup=chatgroup
            message.blob.save(data['blob']['filename'],data['blob']['file_content'])
            
            message.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)  
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        user=self.scope["user"]
        for message in messages:
            if message.author is not user :
                message.seen=True
                message.save()
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        if message.blob :
            return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(timezone.localtime(message.timestamp)),
            'blob':message.blob.url
        }
        else:
            return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(timezone.localtime(message.timestamp)),
            'blob':'null'
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }
    
    def update_user_status(self, user, status):
        user=UserProfile.objects.get(user = user)
        #print(user)
        user.status=status
        user.save()
        return user
    
    def send_status (self):
        chatgroup=ChatGroup.objects.get(id=self.room_name)
        receiver=self.get_group_receiver(chatgroup)
        flag=receiver.profile.status
        print(flag)
        html_status = render_to_string("status.html", {'flag': flag})
        message={
            'html_status':html_status
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        user = self.scope ['user']
        if user.is_authenticated:
            self.update_user_status(user, True)
            self.send_status ()

    def disconnect(self, close_code):
        user = self.scope ['user']
        if user.is_authenticated:
            print("xyz")
            self.update_user_status(user, False)
            self.send_status ()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
       
    def receive(self,text_data=None,bytes_data=None):
        data={}
        filename=None
        #print(text_data)
        if text_data:
            if '.' in text_data:
                self.scope['session']['filename']=text_data
                self.scope['session'].save()
            else:
                #print(text_data)
                data = json.loads(text_data)
                data['blob']=bytes_data
                self.commands[data['command']](self, data)
        
        if (bytes_data):    
            data['blob']=BytesToFile(bytes_data,self.scope['session'].get('filename'))
            data['message']=None
            
            data['from']=self.scope["user"]
            self.commands['new_message'](self, data)
            
        
        
        

    
        
           
        

    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))


    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
    
       
        
