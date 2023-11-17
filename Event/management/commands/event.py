from datetime import datetime
from django.core.management.base import BaseCommand
from Event.models import Event
from EpicEvents.utils import input_validated, request_commands, print_command_result
from EpicEvents.utils import get_object_from_field_name
from EpicEvents.utils import ERROR_MESSAGE
from getpass import getpass


EVENT_FIELD_LIST = [
    'name',
    'ee_contact',
    'date_start',
    'date_end',
    'location',
    'attendees',
    'notes',
    'contract',
    ]

EVENT_DESCRIPTION = {
    'ee_contact': "Nom du contact EpicEvents: ",
    'contract': "Contrat: ",
    'name': "Nom de l'événement: ",
    'date_start': "Date de début [DD/MM/YYYY hh:mm]: ",
    'date_end': "Date de fin [DD/MM/YYYY hh:mm]: ",
    'location': "Lieu: ",
    'attendees': "Nombre de participants: ",
    'notes': "Notes: ",
}

class Command(BaseCommand):
    """create event command"""

    help = 'Commande personnalisée pour effectuer des opérations liées aux événements'

    def add_arguments(self, parser):
        """parsing arguments passed to event command"""
        parser.add_argument('-list', '--list', action='store_true', help='Liste les instances de event')
        parser.add_argument('-read', '--read', action='store_true', help='Lis une instance de event')
        parser.add_argument('-create', '--create', action='store_true', help='Crée une instance de event')
        parser.add_argument('-delete', '--delete', action='store_true', help='Supprime une instance de event')
        parser.add_argument('-update', '--update', action='store_true', help='Mets à jour une instance de event')

    def handle(self, *args, **options):
        """handles 'events related commands'"""
        if options['list']:
            result = self.event_list()
            if result is None:
                print_command_result("Aucun événement trouvé dans la base de donnée")
            else:
                print_command_result("liste des événements :", result)

        elif options['read']:
            event_name = input("Information de l'événement: ")
            event = get_object_from_field_name(
                view_url='event',
                filter_field_name='name',
                filter_field_value=event_name,
                )

            if event is None:
                print_command_result(ERROR_MESSAGE['event_not_existing'])
                return

            # formatting event for terminal output
            event_info = []
            for line in EVENT_FIELD_LIST:
                if line == 'contract':
                    client = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=event['contract'],
                        view_url='contract'
                    )
                    event_info.append(f"{EVENT_DESCRIPTION[line]} {client['information']}")
                elif line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=event['ee_contact'],
                        view_url='user'
                    )
                    event_info.append(f"{EVENT_DESCRIPTION[line]} {user['username']}")
                else:
                    event_info.append(f"{EVENT_DESCRIPTION[line]} {event[line]}")

            print_command_result(printable=event_info)

            return

        elif options['create']:
            event_field_list_create = EVENT_FIELD_LIST

            # gets event's info from user's input
            event_data = {}
            for line in event_field_list_create:
                if line == 'client':
                    client = get_object_from_field_name(
                        filter_field_name='name',
                        filter_field_value=input(EVENT_DESCRIPTION[line]),
                        view_url='client'
                        )
                    event_input = client['id']
                elif line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='username',
                        filter_field_value=input(EVENT_DESCRIPTION[line]),
                        view_url='user'
                    )
                    event_input = user['id']
                else:
                    event_input = input(EVENT_DESCRIPTION[line])

                input_valid = input_validated(event_input)
                if not input_valid:
                    return
                event_data[line] = event_input
            print(event_data)
            result = self.event_create(event_data)

            if result is None:
                print_command_result('Impossible de créer cet événement.')
            else:
                print_command_result(f"Evénement '{event_data['information']}' créé avec succès")

        elif options['delete']:
            event_name = input("Information de l'événement à supprimer: ")
            event = get_object_from_field_name(
                filter_field_name='information',
                filter_field_value=event_name,
                view_url='event'
                )

            if event is None:
                print(ERROR_MESSAGE['event_not_existing'])
                return

            result = self.event_delete(event_id=event['id'])
            if result is None:
                print_command_result("Impossible de supprimer cet événement")
            else:
                print_command_result(f"'{event_name}' supprimé avec succès.")

        elif options['update']:
            event_name = input("Information de l'événement à modifier: ")
            event_data = get_object_from_field_name(
                filter_field_name='information',
                filter_field_value=event_name,
                view_url='event'
                )

            if event_data is None:
                print(ERROR_MESSAGE['event_not_existing'])
                return

            event_description = EVENT_DESCRIPTION
            print('Entrer les valeurs à mettre à jour, laisser vide pour garder les existantes:')

            for line in EVENT_FIELD_LIST:
                if line == 'client':
                    client = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=event_data['client'],
                        view_url='client'
                        )
                    event_description[line] = event_description[line].replace(
                        ':',f" ({client['name']}):")
                elif line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=event_data['ee_contact'],
                        view_url='user'
                    )
                    event_description[line] = event_description[line].replace(
                        ':',f" ({user['username']}):")
                else:
                    event_description[line] = event_description[line].replace(
                        ':',f' ({event_data[line]}):')

                event_input = input(event_description[line])

                # modify the stored value only if user entered something for this line
                if event_input != "" and event_data[line] != event_input:
                    # getting client & ee_contact id from user's input
                    if line == 'client':
                        client = get_object_from_field_name(
                            filter_field_name='name',
                            filter_field_value=event_input,
                            view_url='client'
                            )
                        if client is None:
                            print_command_result(ERROR_MESSAGE['client_not_existing'])
                            return
                        event_data[line] = client['id']
                    elif line == 'ee_contact':
                        user = get_object_from_field_name(
                            filter_field_name='username',
                            filter_field_value=event_input,
                            view_url='user'
                        )
                        if user is None:
                            print_command_result(ERROR_MESSAGE['user_not_existing'])
                            return
                        event_data[line] = user['id']
                    else:
                        event_data[line] = event_input

            result = self.event_update(
                event_id=event_data['id'], event_data=event_data)
            if result is None:
                print_command_result("Impossible de modifier cet événement")
            else:
                print_command_result(f"'{event_name}' modifié avec succès.")


    def event_list(self):
        """
        handles 'listing events
        returns a list of event or None
        '"""
        response = request_commands(view_url='event', operation="read")
        if response is None:
            return None

        event_list = []
        for event_data in response:
            event_list.append(event_data['information'])

        return event_list

    def event_read(self, event_id:int):
        """
        handles reading one event
        returns dict if found or none if not found
        """
        return request_commands(view_url='event', operation="read", object_id=event_id)

    def event_create(self, event_data:dict):
        """handles creating a new event
        gets a dict for event data
        returns 'create if successful'
        """
        return request_commands(view_url='event', operation="create", request_data=event_data)

    def event_delete(self, event_id:int):
        """handles deleting one event
        gets event id (integer)
        returns 'delete' if successful
        """
        return request_commands(view_url='event', operation="delete", object_id=event_id)

    def event_update(self, event_id:int, event_data:dict):
        """handles updating one event
        gets event id (integer)
        returns 'update' if successful
        """
        return request_commands(
            view_url='event', operation="update", request_data=event_data, object_id=event_id)
