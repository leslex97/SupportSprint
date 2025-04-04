from django.apps import AppConfig

class SupportSprintConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SupportSprint'

    def ready(self):
        import SupportSprint.signals