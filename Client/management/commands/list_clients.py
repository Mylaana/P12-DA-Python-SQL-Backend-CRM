from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """handles 'login' command"""
    def handle(self, *args, **options):
        """handles 'login' command"""
        print("liste des clients")