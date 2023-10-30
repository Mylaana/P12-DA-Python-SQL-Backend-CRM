from django.core.management.base import BaseCommand
from Client import models

class Command(BaseCommand):
    """list clients command"""
    def handle(self, *args, **options):
        """handles 'list clients'"""
        print("liste des clients :")
        client_list = models.Client.objects.all()
        for client in client_list:
            print(client.name)
