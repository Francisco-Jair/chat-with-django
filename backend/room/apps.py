from django.apps import AppConfig
from settings.settings import BASE_DIR


class DefaultApp(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.room'
    label = 'room'
    verbose_name = 'room Application'
    path = BASE_DIR / 'backend' / 'room'