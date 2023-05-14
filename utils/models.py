from django.db import models

# Create your models here.
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from user.models import Profile


class Comment(MPTTModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.CharField(max_length=50)  # news: n: ..., chapter: c: ...
    parent = TreeForeignKey('self', null=True, blank=True, related_name='reply', on_delete=models.CASCADE)
    deepth = models.SmallIntegerField(default=0,)
    created_on = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)     # someone should be silent :D
    likes = models.IntegerField(default=0)
    content = models.TextField(max_length=500,)
    media_url = models.CharField(max_length=200, null=True, blank=True)  # image link or smt

    class MPTTMeta:
        order_insertion_by = ['created_on']

    def __str__(self) -> str:
        return f'Comment by {self.author.user.username} at {self.created_on}'


class Notification(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_notifications')

    # null = everyone :D
    receiver = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(default='Đã thông báo', max_length=200,)
    href = models.CharField(default="#", max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True, max_length=500)
    unread = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_on",)

    def __str__(self) -> str:
        return f'Từ {self.sender} tới {self.receiver if self.receiver else "mọi người"} lúc {self.created_on}'

    # def __init__(self, *args, **kwargs) -> None:
    #     if kwargs.get('sender'):
    #         self.sender = kwargs
