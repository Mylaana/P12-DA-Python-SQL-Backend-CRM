from datetime import datetime
from django.core.management.base import BaseCommand
from UserProfile.models import UserProfile
from EpicEvents.utils import input_validated, request_commands, print_command_result
from EpicEvents.utils import get_object_field_from_id, get_object_from_field_name
from getpass import getpass
from EpicEvents.utils import ERROR_MESSAGE


USER_FIELD_LIST_SAFE = [
    'username',
    'team',
    'email',
    'first_name',
    'last_name',
    'phone',
    ]

USER_FIELD_LIST_UNSAFE = [
    'username',
    'password',
    'team',
    'email',
    'first_name',
    'last_name',
    'phone',
    ]

USER_DESCRIPTION = {
    'username': "Nom de l'utilisateur: ",
    'password': "Mot de passe: ",
    'team': "Equipe: ",
    'email': "Email: ",
    'first_name': "Prénom: ",
    'last_name': "Nom de famille: ",
    'phone': "Téléphone: ",
    'last_login': "Dernière connexion: ",
    'is_active': "Compte actif: ",
    'is_staff': "Staff: ",
    'is_admin': "Admin: ",
    'is_superuser': "Superuser: "
}

class Command(BaseCommand):
    """create user command"""

    help = 'Commande personnalisée pour effectuer des opérations liées aux Users'

    def add_arguments(self, parser):
        """parsing arguments passed to user command"""
        parser.add_argument('-list', '--list', action='store_true', help='Liste les instances de user')
        parser.add_argument('-read', '--read', action='store_true', help='Lis une instance de user')
        parser.add_argument('-create', '--create', action='store_true', help='Crée une instance de user')
        parser.add_argument('-delete', '--delete', action='store_true', help='Supprime une instance de user')
        parser.add_argument('-update', '--update', action='store_true', help='Mets à jour une instance de user')

    def handle(self, *args, **options):
        """handles 'users related commands'"""
        if options['list']:
            result = self.user_list()
            if result is None:
                print_command_result("Aucun utilisateur trouvé dans la base de donnée")
            else:
                print_command_result("liste des utilisateurs :", result)

        elif options['read']:
            user_name = input("Nom de l'utilisateur: ")
            user = get_object_from_field_name(
                view_url='user',
                filter_field_name='username',
                filter_field_value=user_name,
                )
            if user is None:
                print_command_result(ERROR_MESSAGE['user_not_existing'])
                return
            team = get_object_field_from_id(
                view_url='team',
                object_id=user['team']
                )

            user_info = []
            for line in USER_FIELD_LIST_SAFE:
                if line == 'team':
                    user_info.append(f"{USER_DESCRIPTION[line]} {team['name']}")
                    continue

                user_info.append(f"{USER_DESCRIPTION[line]} {user[line]}")

            print_command_result(printable=user_info)

            return

        elif options['create']:
            user_field_list_create = USER_FIELD_LIST_UNSAFE

            # gets user's info from user's input
            user_data = {}
            for line in user_field_list_create:
                if line == 'password':
                    user_input = getpass(USER_DESCRIPTION[line])
                elif line == 'team':
                    team = get_object_from_field_name(
                        view_url='team',
                        filter_field_name='name',
                        filter_field_value=input(USER_DESCRIPTION[line])
                        )
                    if team is None:
                        print(ERROR_MESSAGE['team_not_existing'])
                        return None
                    user_input = team['id']
                else:
                    user_input = input(USER_DESCRIPTION[line])

                input_valid = input_validated(user_input)
                if not input_valid:
                    return
                user_data[line] = user_input

            result = self.user_create(user_data)

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result('Impossible de créer cet utilisateur.')
                print(result[-1]['response_text'])
            else:
                print_command_result(f"Utilisateur '{user_data['username']}' créé avec succès")

        elif options['delete']:
            user_name = input("Nom de l'utilisateur à supprimer: ")
            user = get_object_from_field_name(
                view_url='user',
                filter_field_name='username',
                filter_field_value=user_name,
                )
            if user is None:
                print_command_result(ERROR_MESSAGE['user_not_existing'])
                return

            result = self.user_delete(user_id=user['id'])

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result("Impossible de supprimer ce user")
            else:
                print_command_result(f"'{user_name}' supprimé avec succès.")

        elif options['update']:
            user_name = input("Nom de l'utilisateur à modifier: ")
            user_data = get_object_from_field_name(
                view_url='user',
                filter_field_name='username',
                filter_field_value=user_name,
                )
            if user_data is None:
                print_command_result(ERROR_MESSAGE['user_not_existing'])
                return

            # get user data
            user_description = USER_DESCRIPTION
            print('Entrer les valeurs à mettre à jour, laisser vide pour garder les existantes:')

            for line in USER_FIELD_LIST_UNSAFE:
                if line == 'team':
                    team = get_object_field_from_id(
                        view_url='team',
                        object_id=user_data[line]
                        )
                    user_description[line] = user_description[line].replace(
                        ':',f' ({team["name"]}):')
                elif line != 'password':
                    user_description[line] = user_description[line].replace(
                        ':',f' ({user_data[line]}):')

                if line == 'password':
                    user_input = getpass(user_description[line])
                else:
                    user_input = input(user_description[line])

                # modify the stored value only if user entered something
                if user_input != "":
                    user_data[line] = user_input

            result = self.user_update(user_id=user_data['id'], user_data=user_data)

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result("Impossible de modifier cet utilisateur")
            else:
                print_command_result(f"'{user_name}' modifié avec succès.")


    def user_list(self):
        """
        handles 'listing users
        returns a list of user or None
        '"""
        response = request_commands(view_url='user', operation="read")
        response_data = response.pop(-1)
        if response_data['response_status'] != 200 :
            return None

        user_list = []
        for user_data in response:
            user_list.append(user_data['username'])

        return user_list
        
    def user_read(self, user_id:int):
        """
        handles reading one user
        returns dict if found or none if not found
        """
        return request_commands(view_url='user', operation="read", object_id=user_id)

    def user_create(self, user_data:dict):
        """handles creating a new user
        gets a dict for user data
        returns 'create if successful'
        """
        return request_commands(view_url='user', operation="create", request_data=user_data)

    def user_delete(self, user_id:int):
        """handles deleting one user
        gets user id (integer)
        returns 'delete' if successful
        """
        return request_commands(view_url='user', operation="delete", object_id=user_id)

    def user_update(self, user_id:int, user_data:dict):
        """handles updating one user
        gets user id (integer)
        returns 'update' if successful
        """
        return request_commands(view_url='user', operation="update", request_data=user_data, object_id=user_id)
