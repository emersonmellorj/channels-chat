from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe # Remove qualquer inseguranca na string, transformando ela em segura
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from .models import LoggedUser, CustomUser

import json

"""
json.loads() takes in a string and returns a json object. 
json.dumps() takes in a json object and returns a string.
"""

def get_online_users(request, nome_sala):
    data_logged = LoggedUser.objects.all()
    data_logged_user = list()
    if request.method == 'GET':
        for user_logged in data_logged:
            data_logged_user += [(f"username: {user_logged.username}", f"status: {user_logged.status}", f"image: {user_logged.perfil_image}")]        
            users_online = json.dumps(data_logged_user)
            print(users_online)
        return HttpResponse(users_online)


def update_status(request, nome_sala, *args, **kwargs):
    status = request.get_full_path().split('?')[1].split('&')[0].split('=')[1]
    print(status)

    if request.method == 'GET':
        print(f'{request.user}')

        usuario = LoggedUser.objects.get(username=request.user)
        usuario.status=status
        usuario.save()
        msg = 'success'
    else:
        msg = 'error'

    print(usuario.status)
    return HttpResponse(msg)


def get_image_other_user(request, nome_sala):
    """
    Funcao que ira resgatar a url da foto da pessoa que esta mandando mensagem no chat
    """
    other_user_chat = request.get_full_path().split('?')[1].split('&')[0].split('=')[1].replace('%40','@')
    print(f'Other User Name: {other_user_chat}')

    if request.method == 'GET':
        other_user_image = get_user_model().objects.get(username=other_user_chat).perfil_image.url
        print(other_user_image)
        return HttpResponse(other_user_image)


class IndexView(TemplateView):
    template_name = 'index.html'


class SalaView(TemplateView):

    def get_template_names(self):
        """
        Verificando se o usuario esta logado no sistema. 
        Caso seja anonimo, o acesso nao sera concedido
        """
        if self.request.user.is_anonymous:
            print('Usuario nao permitido')
            self.template_name = 'sala.html'
            messages.error(self.request, "Socket closed")
            return [self.template_name]
            #raise PermissionDenied
        else:
            messages.success(self.request, f"Socket open")
            self.template_name = 'sala.html'
            return [self.template_name]


    def get_context_data(self, **kwargs):
        """
        Capturando o contexto da página
        """
        context = super(SalaView, self).get_context_data(**kwargs)
        context["nome_sala_json"] = mark_safe(
            #json.dumps(self.kwargs['nome_sala']) # Transformando JSON recebido em string (objeto pythonico)
            self.kwargs['nome_sala']
        )

        if self.request.user.is_authenticated:
            #context["usuario"] = get_user_model().objects.get(username=self.request.user.username)
            context["usuarios"] = get_user_model().objects.all()
            #context["logged_at"] = get_object_or_404(LoggedUser, username=self.request.user).logged_at
            #context["logados"] = ', '.join([u.username for u in LoggedUser.objects.all()])
            context['user_logados'] = LoggedUser.objects.all()

        print(context)
        return context