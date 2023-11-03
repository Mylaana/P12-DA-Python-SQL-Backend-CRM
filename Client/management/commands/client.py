from datetime import datetime
from django.core.management.base import BaseCommand
from Client.models import Client
from UserProfile.models import UserProfile
from EpicEvents.utils import input_validation, request_commands, print_command_result


class Command(BaseCommand):
    """create client command"""

    help = 'Commande personnalisée pour effectuer des opérations liées aux Clients'

    def add_arguments(self, parser):
        """parsing arguments passed to client command"""
        parser.add_argument('-list', '--list', action='store_true', help='Liste les instances de client')
        parser.add_argument('-read', '--read', action='store_true', help='Lis une instance de client')
        parser.add_argument('-create', '--create', action='store_true', help='Crée une instance de client')
        parser.add_argument('-delete', '--delete', action='store_true', help='Supprime une instance de client')
        parser.add_argument('-update', '--update', action='store_true', help='Mets à jour une instance de client')

    def handle(self, *args, **options):
        """handles 'clients related commands'"""
        if options['list']:
            result = self.client_list()
            if result is None:
                print_command_result("Aucun client trouvé dans la base de donnée")
            else:
                print_command_result("liste des clients :", result)

        elif options['read']:
            result = self.client_read(input("Nom du client: "))
            if result is None:
                print_command_result("Impossible de trouver ce client")
            else:
                print_command_result(printable=result)

        elif options['create']:
            result = self.client_create()

        elif options['delete']:
            self.client_delete()

        elif options['update']:
            self.client_update()


    def client_list(self):
        """
        handles 'listing clients
        returns a list of client or none
        '"""
        response = request_commands(view_url='client', operation="get")
        if response is None:
            return None

        client_list = []

        for client_data in response:
            client_list.append(client_data['name'])

        return client_list

    def client_read(self, client_name):
        """
        handles reading one client
        returns client info if found or none
        """
        response = request_commands(view_url='client', operation="get")

        if response is None:
            return None

        for line in response:
            if client_name == line['name']:
                client_info = []
                ee_contact_id = line['ee_contact']
                ee_contact_name = self.get_ee_contact_name(ee_contact_id)
                client_info.append(f"Client: {line['name']}")
                client_info.append(f"Epic Events - Contact: {ee_contact_name}")
                client_info.append(f"Client - Numero Siren: {line['siren']}")
                client_info.append(f"Client - Nom du contact: {line['client_contact_name']}")
                client_info.append(f"Client - Email: {line['email']}")
                client_info.append(f"Client - Téléphone: {line['phone']}")
                client_info.append(f"Client - Information: {line['information']}")

                return client_info

    def client_create(self):
        """handles creating a new client"""
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

        return request_commands(view_url='client', operation="create", request_data=data)
        
    def client_delete(self):
        """handles deleting one client"""
        print("delete")

    def client_update(self):
        """handles updating one client"""
        print("update")

    def get_ee_contact_id(self, contact_name:str):
        """gets username returns user id"""
        result = UserProfile.objects.filter(username=contact_name).first().id
        return result

    def get_ee_contact_name(self, contact_id:int):
        """gets username returns user id"""
        result = UserProfile.objects.filter(id=contact_id).first().id
        return result
