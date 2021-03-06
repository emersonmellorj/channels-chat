from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.utils.safestring import mark_safe # Remove qualquer inseguranca na string, transformando ela em segura
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import LoggedUser, CustomUser

from .forms import CustomUserCreateForm, SignUpForm

import json

"""
json.loads() takes in a string and returns a json object. 
json.dumps() takes in a json object and returns a string.
#json.dumps(self.kwargs['nome_sala']) # Transformando JSON recebido em string (objeto pythonico)
"""

def get_online_users(request, nome_sala):
    data_logged = LoggedUser.objects.filter(room_name=nome_sala)
    data_logged_user = list()
    if request.method == 'GET':
        for user_logged in data_logged:
            data_logged_user += [(f"username: {user_logged.username}", f"status: {user_logged.status}", f"image: {user_logged.perfil_image}")]        
            users_online = json.dumps(data_logged_user)
            print(users_online)
        return HttpResponse(users_online)


def update_status(request, nome_sala, *args, **kwargs):
    status = request.get_full_path().split('?')[1].split('&')[0].split('=')[1]
    if request.method == 'GET':
        usuario = LoggedUser.objects.get(username=request.user)
        usuario.status=status
        usuario.save()
        msg = 'success'
    else:
        msg = 'error'
    return HttpResponse(msg)


def get_image_other_user(request, nome_sala):
    """
    Funcao que ira resgatar a url da foto da pessoa que esta mandando mensagem no chat
    """
    other_user_chat = request.get_full_path().split('?')[1].split('&')[0].split('=')[1].replace('%40','@')
    if request.method == 'GET':
        other_user_image = get_user_model().objects.get(username=other_user_chat).perfil_image.url
        return HttpResponse(other_user_image)


class SigUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'signup_form.html'
    success_url = reverse_lazy('login')

    # Metodo de FormView
    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Conta criada sucesso!')
        return super(SigUpView, self).form_valid(form, *args, **kwargs) # Status Code 302

    # Metodo de FormView
    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro na criação da conta!')
        return super(SigUpView, self).form_invalid(form, *args, **kwargs) # Status Code 200


class IndexView(TemplateView):
    template_name = 'index.html'


class SalaView(TemplateView):

    def get_template_names(self):
        """
        Verificando se o usuario esta logado no sistema. 
        Caso seja anonimo, o acesso nao sera concedido
        """
        
        # Contando a quantidade de usuarios na sala
        room_name = self.kwargs['nome_sala']
        count_users_chat = LoggedUser.objects.filter(room_name=room_name).count()

        # So irei tentar pegar o nome da sala e contagem de usuarios se user estiver
        if not self.request.user.is_anonymous:
            me = get_object_or_404(LoggedUser, username=self.request.user.username)
            my_room_name = me.room_name

        # Usuario anonimo nao podera participar da sala
        if self.request.user.is_anonymous:
            print('Usuario nao permitido')
            self.template_name = 'sala.html'
            messages.error(self.request, "Socket closed")
            return [self.template_name]
            
        elif count_users_chat > 1 and my_room_name != room_name:
            self.template_name = 'index.html'
            messages.error(self.request, f"A sala {room_name} já esta na sua capacidade máxima ({count_users_chat} usuários).")
            return [self.template_name]

        else:
            messages.success(self.request, f"Socket open")
            self.template_name = 'sala.html'

            # Armazendo o nome da sala que estou logado
            if me:
                me.room_name = self.kwargs['nome_sala']
                me.save()

            return [self.template_name]


    def get_context_data(self, **kwargs):
        """
        Capturando o contexto da página
        """
        context = super(SalaView, self).get_context_data(**kwargs)
        context["nome_sala_json"] = mark_safe(
            self.kwargs['nome_sala']
        )

        if self.request.user.is_authenticated:
            context["usuarios"] = get_user_model().objects.all()
            context['user_logados'] = LoggedUser.objects.filter(room_name=self.kwargs['nome_sala'])

        return context