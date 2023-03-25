import os

from django.db import models
from django.contrib.auth.models import User

from colorfield.fields import ColorField

# Create your models here.


def avatar_image_path(self, filename):
    return os.path.join("user", "avatar", self.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="user", related_name="profile")
    display_name = models.CharField(verbose_name="Tên hiển thị", max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_image_path, blank=True)
    description = models.TextField(verbose_name="Mô tả", max_length=500, blank=True)

    theme = models.CharField("Giao diện", max_length=50, default='Dark', )
    interface_color = ColorField(default='#3A3F44')
    text_color = ColorField(default='#272B30')
    accent_color = ColorField(default='#B2DFFB')
    reader_background = ColorField(default='#EEEEEE')

    mute = models.BooleanField(default=False, help_text="Mấy thằng này tốt nhất là nên nín =))")

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name_plural = "Hồ sơ"

    def valid_theme(theme: str):
        return theme in ['Dark', 'Reaper', 'Zaibatsu', 'Light', 'Custom']