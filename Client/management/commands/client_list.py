from django.core.management.base import BaseCommand
from Client import models
from EpicEvents.utils import request_commands

class Command(BaseCommand):
    """list client command"""
    def handle(self, *args, **options):
        """handles 'listing clients'"""
        response = request_commands(view_url='client', is_get_request=True)
        if response is None:
            print("Aucun client trouvé dans la base de donnée")
            return

        print("liste des clients :")
        for client_data in response:
            print(client_data['name'])
