from django.apps import AppConfig


class NewspipeAppConfig(AppConfig):
    name = 'newspipe'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from newspipe import celery  # noqa
