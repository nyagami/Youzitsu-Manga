from django.apps import AppConfig


class MiscConfig(AppConfig):
    name = "misc"
    verbose_name = "News"

    def ready(self):
        import misc.signals  # noqa
