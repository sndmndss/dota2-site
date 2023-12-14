from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'd2site.apps.home'
    verbose_name = 'homepage'

    def ready(self):
        import d2site.apps.home.signals
