from django.urls import path

from .views import IndexView, SalaView, update_status, get_image_other_user

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('chat/<str:nome_sala>/', SalaView.as_view(), name='sala'),
    path('chat/<str:nome_sala>/status', update_status, name='status'),
    path('chat/<str:nome_sala>/get_image_other_user', get_image_other_user, name='get_image_other_user')
]
