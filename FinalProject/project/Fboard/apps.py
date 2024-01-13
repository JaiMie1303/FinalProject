from django.apps import AppConfig


class FboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Fboard'

    def ready(self):
        import Fboard.signals

