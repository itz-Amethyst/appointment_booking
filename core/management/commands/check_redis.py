from django.core.management.base import BaseCommand
from django_redis import get_redis_connection
import logging

class Command(BaseCommand):
    help = 'Check if Redis is available'

    def handle(self, *args, **kwargs):
        try:
            conn = get_redis_connection()
            conn.ping()
            self.stdout.write(self.style.SUCCESS('Redis is available'))
        except Exception as e:
            logging.error('Redis is not available: %s', e)
            self.stdout.write(self.style.ERROR('Redis is not available'))
            raise e