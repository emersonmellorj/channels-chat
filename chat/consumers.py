from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login, get_user
from asgiref.sync import sync_to_async, async_to_sync

import datetime

import json

"""
json.loads() takes in a string and returns a json object. 
json.dumps() takes in a json object and returns a string.
"""

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Comunicacao asyncrona 
    """

    async def connect(self):

        if self.scope['user'].is_authenticated:

            print(self.scope['url_route'])
            self.user = self.scope['user']
            self.room_name = self.scope['url_route']['kwargs']['nome_sala']
            self.room_group_name = f'chat_{self.room_name}'
            print(self.room_group_name)

            """
            Todos os comandos dentro da funcao que dependem de alguma entrada ou saida precisamos utilizar o await
            Espere algo ser executado
            """

            # Entrar na sala
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        

    async def disconnect(self, code):

        if self.scope['user'].is_authenticated:
            # Sai da sala
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )


    async def receive(self, text_data):
        """
        Recebe mensagem do Websocket quando um cliente envia uma mensagem para a sala
        """
        text_data_json = json.loads(text_data) # Transformando o texto recebido em Json
        mensagem = text_data_json['mensagem']

        data_atual = datetime.datetime.now()
        data_br = data_atual.strftime("%H:%M:%S")
        print(data_br)

        # Envia a mensagem para a sala
        await self.channel_layer.group_send(
            self.room_group_name, # nome da sala
            {
                'type': 'chat_message',
                "username": self.scope["user"].username,
                'message': f"{mensagem}"
            }
        )


    async def chat_message(self, event):
        """
        Recebe a mensagem do grupo da sala (chamada quando uma mensagem e enviada para o grupo)
        """
        print(f'Event:{event}')
        print("\npassei em chat_message ...\n")
        mensagem = event['message']
        author = event['username']

        # Envia a mensagem para o websocket
        await self.send(text_data=json.dumps({
            'mensagem': mensagem,
            'author': author
        }))