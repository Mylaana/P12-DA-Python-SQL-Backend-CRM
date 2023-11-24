from django.core.management.base import BaseCommand
from getpass import getpass
from EpicEvents.authentication import request_get_token, write_token

class Command(BaseCommand):
    """handles 'login' command"""
    def handle(self, *args, **options):
        """handles 'login' command"""

        auth_data = request_get_token()
        if auth_data['token'] is not None:
            print(f"Vous êtes authentifié, bienvenue {auth_data['username']}")
            write_token(auth_data)
