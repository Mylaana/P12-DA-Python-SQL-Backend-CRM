from datetime import datetime
from django.core.management.base import BaseCommand
from Client.models import Client
from UserProfile.models import UserProfile
from EpicEvents.utils import input_validation, request_commands


class Command(BaseCommand):
    """create client command"""
    def handle(self, *args, **options):
        """handles 'creating new client'"""
        # ask contact name and get contact id from it
        ee_contact = self.get_ee_contact_id(input('Epic Events - Nom du contact: '))
        if input_validation(ee_contact):
            return

        if ee_contact is None:
            print("Impossible de trouver cet utilisateur dans la base de données.")
            return

        # ask client infos
        name = input('Client - Nom: ')
        if input_validation(name):
            return

        siren = input('Client - Numero Siren: ')
        if input_validation(siren):
            return

        client_contact_name = input('Client - Nom du contact: ')
        if input_validation(client_contact_name):
            return

        email = input('Client - Email: ')
        if input_validation(email):
            return

        phone = input('Client - Téléphone: ')
        if input_validation(phone):
            return

        information = input('Client - Information: ')
        if input_validation(siren):
            return

        data = {
            'ee_contact': ee_contact,
            'name': name,
            'siren': siren,
            'client_contact_name': client_contact_name,
            'email': email,
            'phone': phone,
            'information': information,
        }

        request_commands(view_url='client', operation="create", request_data=data)


    def get_ee_contact_id(self, contact_name:str):
        contact_id = UserProfile.objects.filter(username=contact_name).first().id
        return contact_id
