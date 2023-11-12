from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import ws_urlpatterns
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CurioSpace.settings')
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns)),
})
