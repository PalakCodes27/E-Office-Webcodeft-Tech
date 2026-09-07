import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "office_management.settings"
)

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


django_application = get_asgi_application()


from core.routing import websocket_urlpatterns


application = ProtocolTypeRouter({

    "http": django_application,

    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),

})