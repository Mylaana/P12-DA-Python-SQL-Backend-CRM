from django.core.management.base import BaseCommand
from getpass import getpass
from EpicEvents.authentication import request_logout

class Command(BaseCommand):
    """handles 'login' command"""
    def handle(self, *args, **options):
        """handles 'login' command"""
        result = request_logout()
        if result.status_code == 200:
            print("Vous êtes maintenant déconnecté.")
        else:
            print("Déconnexion impossible.")
