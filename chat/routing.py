from django.urls import path

from .consumers import *

ws_urlpatterns = [
    path('ws/chat/<int:id>/', WSChatView.as_asgi())
]
