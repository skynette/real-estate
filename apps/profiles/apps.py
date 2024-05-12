from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'apps.profiles'

    def ready(self):
        from apps.profiles import signals
