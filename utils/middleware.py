from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from django.db.models import Q
from .models import Notification


class NotifactionMiddleWare(MiddlewareMixin):

    def process_request(self, request: HttpRequest):
        profile = request.user.profile if request.user.is_authenticated else None
        notifications = Notification.objects.filter(
            Q(receiver=None) | Q(receiver=profile)
        ).order_by('-created_on')
        for notification in notifications:
            notification.created_on = f'{notification.created_on.date()} {notification.created_on.time()}'
        request.notifications = notifications
        request.new_noti = notifications.filter(unread=True)
