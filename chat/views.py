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
            context["usuario"] = get_user_model().objects.get(username=self.request.user.username)
            context["logged_at"] = get_object_or_404(LoggedUser, username=self.request.user).logged_at
            context["logados"] = ', '.join([u.username for u in LoggedUser.objects.all()])
            context['user_logados'] = LoggedUser.objects.all()

        print(context)
        return context


"""
This is an example view in views.py that shows all logged users
"""
# from django.shortcuts import render    
# def logged(request):
#     logged_users = LoggedUser.objects.all().order_by('username')
#     context = {'logged_users': logged_users}
#     return render('users/logged.html', context)