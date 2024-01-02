from django.apps import AppConfig


class ObrabackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'obraBack'
    def ready(self):
        import obraBack.signals
