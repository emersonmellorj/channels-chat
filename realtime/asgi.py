"""
ASGI config for realtime project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from dj_static import Cling, MediaCling
from channels.layers import get_channel_layer
import channels.asgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime.settings')

channel_layer = channels.asgi.get_channel_layer()

application = Cling(MediaCling(get_asgi_application()))
