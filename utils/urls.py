
from django.urls import re_path
from .consumers import NotifcationConsumer, CommentConsumer

websocket_urlpatterns = [
    re_path(r'ws/(?P<usernam>[a-zA-Z]+)/$', NotifcationConsumer.as_asgi, name='notification_ws'),
    re_path(r'ws/(?P<article>^[a-z]:[\w-]+)/$', CommentConsumer.as_asgi, name='comment_ws'),
]
