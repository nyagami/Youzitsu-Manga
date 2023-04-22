import os

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from colorfield.fields import ColorField

# Create your models here.


def avatar_image_path(self, filename):
    return os.path.join("user", "avatar", self.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="user", related_name="profile")
    display_name = models.CharField(verbose_name="Tên hiển thị", max_length=50, blank=True, null=True)
    avatar = models.CharField(default="/static/img/unknown_user.jpeg", max_length=200, blank=True, null=True)
    description = models.TextField(verbose_name="Mô tả", max_length=500, blank=True)

    theme = models.CharField("Giao diện", max_length=50, default='Dark')
    primary_color = ColorField(default='#3A3F44')
    text_color = ColorField(default='#272B30')
    accent_color = ColorField(default='#B2DFFB')
    reader_background = ColorField(default='#EEEEEE')

    mute = models.BooleanField(default=False, help_text="Mấy thằng này tốt nhất là nên nín =))")

    def __str__(self) -> str:
        return self.display_name

    @classmethod
    def valid_theme(self, theme: str):
        if theme not in ['Dark', 'Reaper', 'Zaibatsu', 'Light', 'Custom']:
            raise ValidationError

    def reset_theme(self):
        self.primary_color = '#3A3F44'
        self.text_color = '#B2DFFB'
        self.accent_color = '#B2DFFB'
        self.reader_background = '#EEEEEE'
        self.save()
