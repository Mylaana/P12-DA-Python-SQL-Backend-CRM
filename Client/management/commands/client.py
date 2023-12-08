from datetime import datetime
from django.core.management.base import BaseCommand
from Client.models import Client
from UserProfile.models import UserProfile
from EpicEvents.utils import input_validated, request_commands, print_command_result
from EpicEvents.utils import get_object_from_field_name, get_date_time_from_user
from EpicEvents.utils import ERROR_MESSAGE

CLIENT_FIELD_LIST = [
    'ee_contact',
    'name',
    'siren',
    'client_contact_name',
    'email',
    'phone',
    'information'
    ]

CLIENT_DESCRIPTION = {
    'ee_contact': "Epic Events - Nom du contact: ",
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
        parser.add_argument('-own', '--own', action='store_true', help='filtre la liste sur les clients qui vous sont attribués')
        parser.add_argument('-read', '--read', action='store_true', help='Lis une instance de client')
        parser.add_argument('-create', '--create', action='store_true', help='Crée une instance de client')
        parser.add_argument('-delete', '--delete', action='store_true', help='Supprime une instance de client')
        parser.add_argument('-update', '--update', action='store_true', help='Mets à jour une instance de client')

    def handle(self, *args, **options):
        """handles 'clients related commands'"""
        if options['list']:
            result = self.client_list(options['own'])
            if result is None:
                print_command_result("Aucun client trouvé dans la base de donnée")
            else:
                print_command_result("liste des clients :", result)

        elif options['read']:
            client_name = input("Nom du client: ")
            client = get_object_from_field_name(
                view_url='client',
                filter_field_name='name',
                filter_field_value=client_name,
                )

            if client is None:
                print_command_result(ERROR_MESSAGE['client_not_existing'])
                return

            # formatting event for terminal output
            event_info = []
            for line in CLIENT_FIELD_LIST:
                if line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=client['ee_contact'],
                        view_url='user'
                    )
                    event_info.append(f"{CLIENT_DESCRIPTION[line]} {user['username']}")
                else:
                    event_info.append(f"{CLIENT_DESCRIPTION[line]} {client[line]}")

            print_command_result(printable=event_info)

            return

        elif options['create']:
            client_field_list_create = CLIENT_FIELD_LIST

            # gets client's info from user's input
            client_data = {}
            for line in client_field_list_create:
                if line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='username',
                        filter_field_value=input(CLIENT_DESCRIPTION[line]),
                        view_url='user'
                    )
                    if  user is None:
                        print(ERROR_MESSAGE['user_not_existing'])
                        return None

                    client_input = user['id']
                elif 'date' in line:
                    print(CLIENT_DESCRIPTION[line])
                    client_input = str(get_date_time_from_user())
                else:
                    client_input = input(CLIENT_DESCRIPTION[line])

                input_valid = input_validated(client_input)
                if not input_valid:
                    return
                client_data[line] = client_input

            result = self.client_create(client_data)

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result('Impossible de créer cet événement.')
                print(result[-1]['response_text'])
            else:
                print_command_result(f"Evénement '{client_data['name']}' créé avec succès")

        elif options['delete']:
            client_name = input("Information de l'événement à supprimer: ")
            client = get_object_from_field_name(
                filter_field_name='name',
                filter_field_value=client_name,
                view_url='client'
                )

            if client is None:
                print(ERROR_MESSAGE['client_not_existing'])
                return

            result = self.client_delete(client_id=client['id'])

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result("Impossible de supprimer ce client")
            else:
                print_command_result(f"'{client_name}' supprimé avec succès.")

        elif options['update']:
            client_name = input("Nom du client à modifier: ")
            client_data = get_object_from_field_name(
                filter_field_name='name',
                filter_field_value=client_name,
                view_url='client'
                )

            if client_data is None:
                print(ERROR_MESSAGE['client_not_existing'])
                return

            client_description = CLIENT_DESCRIPTION
            print('Entrer les valeurs à mettre à jour, laisser vide pour garder les existantes:')

            for line in CLIENT_FIELD_LIST:
                if line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=client_data['ee_contact'],
                        view_url='user'
                    )
                    client_description[line] = client_description[line].replace(
                        ':',f" ({user['username']}):")
                else:
                    client_description[line] = client_description[line].replace(
                        ':',f' ({client_data[line]}):')

                client_input = input(client_description[line])

                # modify the stored value only if user entered something for this line
                if client_input != "" and client_data[line] != client_input:
                    # getting contract & ee_contact id from user's input
                    if line == 'contract':
                        contract = get_object_from_field_name(
                            filter_field_name='name',
                            filter_field_value=client_input,
                            view_url='contract'
                            )
                        if contract is None:
                            print_command_result(ERROR_MESSAGE['contract_not_existing'])
                            return
                        client_data[line] = contract['id']
                    elif line == 'ee_contact':
                        user = get_object_from_field_name(
                            filter_field_name='username',
                            filter_field_value=client_input,
                            view_url='user'
                        )
                        if user is None:
                            print_command_result(ERROR_MESSAGE['user_not_existing'])
                            return
                        client_data[line] = user['id']
                    else:
                        client_data[line] = client_input

            result = self.client_update(
                client_id=client_data['id'], client_data=client_data)

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result("Impossible de modifier ce client")
            else:
                print_command_result(f"'{client_name}' modifié avec succès.")

    def client_list(self, own:bool=False):
        """
        handles 'listing clients
        returns a list of client or None
        '"""
        response = request_commands(view_url='client', operation="read")
        response_data = response.pop(-1)
        if response_data['response_status'] != 200 :
            return None

        client_list = []

        for client_data in response:
            if client_data['ee_contact_name'] == response_data['request_username'] or own == False:
                client_list.append(client_data['name'])

        if client_list == []:
            client_list = None

        return client_list

    def client_create(self, client_data):
        """handles creating a new client"""
        return request_commands(view_url='client', operation="create", request_data=client_data)

    def client_delete(self, client_id):
        """handles deleting one client"""
        return request_commands(view_url='client', operation="delete", object_id=client_id)

    def client_update(self, client_id, client_data):
        """handles updating one client"""
        return request_commands(view_url='client', operation="update", request_data=client_data, object_id=client_id)
