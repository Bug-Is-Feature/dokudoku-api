from django.apps import AppConfig
from django.conf import settings

class CronjobsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cronjobs"

    def ready(self):
        if not settings.DEBUG and not settings.TESTING:
            from . import updater
            updater.start()
