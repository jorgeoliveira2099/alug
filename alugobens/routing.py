

from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from Chat.consumers import *

import Chat.routing


application = ProtocolTypeRouter({    
    'websocket': AuthMiddlewareStack(
        URLRouter(
            Chat.routing.websocket_urlpatterns
        )
    ),
   
})
    