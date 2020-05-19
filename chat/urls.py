from django.urls import path

from .views import IndexView, SalaView, update_status

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('chat/<str:nome_sala>/', SalaView.as_view(), name='sala'),
    path('chat/<str:nome_sala>/status', update_status, name='status'),
]
