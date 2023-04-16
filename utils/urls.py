
from django.urls import re_path
from .consumers import NotifcationConsumer, CommentConsumer

websocket_urlpatterns = [
    re_path(r'ws/comment/(?P<type>([a-z]))/(?P<article>[\w-]+)/$', CommentConsumer.as_asgi(), name='comment_ws'),
    re_path(r'ws/(?P<username>[a-zA-Z]+)/$', NotifcationConsumer.as_asgi(), name='notification_ws'),
]
