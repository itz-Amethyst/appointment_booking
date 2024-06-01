from django.apps import AppConfig
from django.core.management import call_command


def check_redis_on_startup():
    try:
        call_command('check_redis')
    except Exception as e:
        raise e

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready( self ):
        import core.signals
        # TODO
        # check_redis_on_startup()

