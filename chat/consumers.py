from channels.generic.websocket import AsyncWebsocketConsumer

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
        self.user = self.scope['user']
        print(self.user)
        self.room_name = self.scope['url_route']['kwargs']['nome_sala']
        self.room_group_name = f'chat_{self.room_name}'

        # Entrar na sala
        """
        Todos os comandos dentro da funcao que dependem de alguma entrada ou saida precisamos utilizar o await
        Espere algo ser executado
        """
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        # Sai da sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Recebe mensagem do Websocket
        """
        text_data_json = json.loads(text_data) # Transformando o texto recebido em Json
        mensagem = text_data_json['mensagem']

        # Envia a mensagem para a sala
        await self.channel_layer.group_send(
            self.room_group_name, # nome da sala
            {
                'type': 'chat_message',
                'message': mensagem
            }
        )

    async def chat_message(self, event):
        """
        Recebe a mensagem da sala
        """
        mensagem = event['message']

        # Envia a mensagem para o websocket
        await self.send(text_data=json.dumps({
            'mensagem': mensagem
        }))