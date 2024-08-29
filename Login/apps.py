# apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'Login'

    def ready(self):
        import Login.signals
