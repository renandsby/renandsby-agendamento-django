from django.apps import AppConfig


class AdolescentesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adolescentes'

    def ready(self):
        from . import signals