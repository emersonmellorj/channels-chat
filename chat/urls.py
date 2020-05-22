from django.urls import path, include
from django.conf import settings

from .views import IndexView, SalaView, update_status, get_image_other_user, get_online_users, SigUpView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('chat/<str:nome_sala>/', SalaView.as_view(), name='sala'),
    path('chat/<str:nome_sala>/status', update_status, name='status'),
    path('chat/<str:nome_sala>/get_image_other_user', get_image_other_user, name='get_image_other_user'),
    path('chat/<str:nome_sala>/get_online_users', get_online_users, name='get_online_users'),
    path('contas/', include('django.contrib.auth.urls')),
    path('contas/signup', SigUpView.as_view(), name='signup'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
