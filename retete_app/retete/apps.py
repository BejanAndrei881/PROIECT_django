from django.apps import AppConfig


class ReteteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'retete'


class YourAppConfig(AppConfig):
    name = 'retete'

    def ready(self):
        import retete.signals