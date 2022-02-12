from django.apps import AppConfig


class AbpStepsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.abp_steps'

    def ready(self):
        import applications.abp_steps.signals