from django.db import models

# Create your models here.
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from user.models import Profile


class Comment(MPTTModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.CharField(max_length=50)  # news: n: ..., chapter: c: ...
    parent = TreeForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    mention = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='mentions')    # The one who is replied or noone
    deepth = models.SmallIntegerField(default=0,)
    created_on = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)     # someone should be silent :D
    likes = models.IntegerField(default=0)
    content = models.TextField(max_length=500,)
    media_url = models.CharField(max_length=50, null=True, blank=True)  # image link or smt

    class MPTTMeta:
        order_insertion_by = ['-created_on']

    def __str__(self) -> str:
        return f'Comment by {self.author.user.username} at {str(self.created_on)}'

    # def comment_time(self)    -> should be implemented in frontend
