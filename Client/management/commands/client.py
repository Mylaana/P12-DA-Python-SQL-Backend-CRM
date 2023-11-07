from datetime import datetime
from django.core.management.base import BaseCommand
from Client.models import Client
from UserProfile.models import UserProfile
from EpicEvents.utils import input_validated, request_commands, print_command_result
from EpicEvents.utils import get_ee_client_id, get_ee_contact_id, get_ee_contact_name


CLIENT_FIELD_LIST = [
    'name',
    'siren',
    'client_contact_name',
    'email',
    'phone',
    'information'
    ]

CLIENT_DESCRIPTION = {
    'ee_contact_name': "Epic Events - Nom du contact: ",
    'ee_contact_id': "Epic Events - ID du contact: ",
    'name': "Client - Nom: ",
    'siren': "Client - Numero Siren: ",
    'client_contact_name': "Client - Nom du contact: ",
    'email': "Client - Email: ",
    'phone': "Client - Téléphone: ",
    'information':"Client - Information: "
}

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
            client_name = input("Nom du client: ")
            client_id = get_ee_client_id(client_name=client_name)
            if client_id is None:
                print_command_result("Impossible de trouver ce client")
                return

            result = self.client_read(client_id=client_id)

            client_info = []
            client_info.append(f"Client: {result['name']}")
            client_info.append(f"Epic Events - Contact: {result['ee_contact_name']}")
            client_info.append(f"Client - Numero Siren: {result['siren']}")
            client_info.append(f"Client - Nom du contact: {result['client_contact_name']}")
            client_info.append(f"Client - Email: {result['email']}")
            client_info.append(f"Client - Téléphone: {result['phone']}")
            client_info.append(f"Client - Information: {result['information']}")

            print_command_result(printable=client_info)

            return

        elif options['create']:
            # ask contact name and get contact id from it
            ee_contact_name = input('Epic Events - Nom du contact: ')
            ee_contact_id = get_ee_contact_id(ee_contact_name)

            if ee_contact_id is None:
                print("Impossible de trouver cet utilisateur dans la base de données.")
                return

            client_data = {
                'ee_contact': ee_contact_id,
                'name': "",
                'siren': "",
                'client_contact_name': "",
                'email': "",
                'phone': "",
                'information':""
            }

            # gets client's info from user's input
            for line in CLIENT_FIELD_LIST:
                user_input = input(CLIENT_DESCRIPTION[line])
                input_valid = input_validated(user_input)
                if not input_valid:
                    return
                client_data[line] = user_input

            result = self.client_create(client_data)

            if result is None:
                print_command_result('Impossible de créer ce client.')
            else:
                print_command_result(f"Client '{client_data['name']}' créé avec succès")

        elif options['delete']:
            client_name = input("Nom du client à supprimer: ")
            client_id = get_ee_client_id(client_name=client_name)

            if client_id is None:
                print("Impossible de trouver ce client dans la base de données.")
                return

            result = self.client_delete(client_id=client_id)
            if result is None:
                print_command_result("Impossible de supprimer ce client")
            else:
                print_command_result(f"'{client_name}' supprimé avec succès.")

        elif options['update']:
            client_name = input("Nom du client à modifier: ")
            client_id = get_ee_client_id(client_name=client_name)

            if client_id is None:
                print("Impossible de trouver ce client dans la base de données.")
                return

            # get client data
            client_data = self.client_read(client_id)
            client_description = CLIENT_DESCRIPTION
            print('Entrer les valeurs à mettre à jour, laisser vide pour garder les existantes:')
            for line in CLIENT_FIELD_LIST:
                client_description[line] = client_description[line].replace(':',f' ({client_data[line]}):' )
                user_input = input(client_description[line])

                # modify the stored value only if user entered something
                if user_input != "":
                    client_data[line] = user_input

            result = self.client_update(client_id=client_id, client_data=client_data)
            if result is None:
                print_command_result("Impossible de modifier ce client")
            else:
                print_command_result(f"'{client_name}' modifié avec succès.")


    def client_list(self):
        """
        handles 'listing clients
        returns a list of client or None
        '"""
        response = request_commands(view_url='client', operation="read")
        if response is None:
            return None

        client_list = []

        for client_data in response:
            client_list.append(client_data['name'])

        return client_list

    def client_read(self, client_id):
        """
        handles reading one client
        returns dict if found or none if not found
        """
        response = request_commands(view_url='client', operation="read", id=client_id)
        client_info = []
        ee_contact_id = int(response['ee_contact'])
        ee_contact_name = get_ee_contact_name(ee_contact_id)

        client_info = {
            'ee_contact_id': ee_contact_id,
            'ee_contact_name': ee_contact_name,
            'name': response['name'],
            'siren': response['siren'],
            'client_contact_name': response['client_contact_name'],
            'email': response['email'],
            'phone': response['phone'],
            'information': response['information'],
        }
        return client_info

    def client_create(self, client_data):
        """handles creating a new client"""

        return request_commands(view_url='client', operation="create", request_data=client_data)

    def client_delete(self, client_id):
        """handles deleting one client"""
        return request_commands(view_url='client', operation="delete", id=client_id)

    def client_update(self, client_id, client_data):
        """handles updating one client"""
        return request_commands(view_url='client', operation="update", request_data=client_data, id=client_id)
