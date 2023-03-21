from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from utils.models import Comment

# Register your models here.


class CommentAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


admin.site.register(Comment, CommentAdmin)
