from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe # Remove qualquer inseguranca na string, transformando ela em segura

import json

"""
json.loads() takes in a string and returns a json object. 
json.dumps() takes in a json object and returns a string.
"""

class IndexView(TemplateView):
    template_name = 'index.html'


class SalaView(TemplateView):
    template_name = 'sala.html'

    def get_context_data(self, **kwargs):
        print(self.kwargs)
        context = super(SalaView, self).get_context_data(**kwargs)
        context["nome_sala_json"] = mark_safe(
            json.dumps(self.kwargs['nome_sala']) # Transformando JSON recebido em string (objeto pythonico)
        )

        return context
    