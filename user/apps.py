from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    verbose_name = "Người dùng"

    def ready(self) -> None:
        import user.signals
