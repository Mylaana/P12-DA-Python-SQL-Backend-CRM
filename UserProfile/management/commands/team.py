from datetime import datetime
from django.core.management.base import BaseCommand
from UserProfile.models import UserProfile
from EpicEvents.utils import input_validated, request_commands, print_command_result
from EpicEvents.utils import get_object_from_field_name, get_date_time_from_user
from EpicEvents.utils import ERROR_MESSAGE

TEAM_FIELD_LIST = [
    'name'
    ]

TEAM_DESCRIPTION = {
    'name': "Nom de l'équipe: "
}

class Command(BaseCommand):
    """create team command"""

    help = 'Commande personnalisée pour effectuer des opérations liées aux équipes'

    def add_arguments(self, parser):
        """parsing arguments passed to team command"""
        parser.add_argument('-list', '--list', action='store_true', help='Liste les instances de team')
        parser.add_argument('-read', '--read', action='store_true', help='Lis une instance de team')
        parser.add_argument('-create', '--create', action='store_true', help='Crée une instance de team')
        parser.add_argument('-delete', '--delete', action='store_true', help='Supprime une instance de team')
        parser.add_argument('-update', '--update', action='store_true', help='Mets à jour une instance de team')

    def handle(self, *args, **options):
        """handles 'teams related commands'"""
        if options['list']:
            result = self.team_list()
            if result is None:
                print_command_result("Aucune équipe trouvée dans la base de donnée")
            else:
                print_command_result("liste des équipes :", result)

        elif options['read']:
            team_name = input("Nom de l'équipe: ")
            team = get_object_from_field_name(
                view_url='team',
                filter_field_name='name',
                filter_field_value=team_name,
                )

            if team is None:
                print_command_result(ERROR_MESSAGE['team_not_existing'])
                return

            # formatting team for terminal output
            team_info = []
            for line in TEAM_FIELD_LIST:
                team_info.append(f"{TEAM_DESCRIPTION[line]} {team[line]}")

            print_command_result(printable=team_info)

        elif options['create']:
            team_field_list_create = TEAM_FIELD_LIST

            # gets team's info from user's input
            team_data = {}
            for line in team_field_list_create:
                team_input = input(TEAM_DESCRIPTION[line])

                input_valid = input_validated(team_input)
                if not input_valid:
                    return
                team_data[line] = team_input

            result = self.team_create(team_data)

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result('Impossible de créer cette équipe.')
                print(result[-1]['response_text'])
            else:
                print_command_result(f"Evénement '{team_data['name']}' créé avec succès")

        elif options['delete']:
            team_name = input("Nom de l'équipe à supprimer: ")
            team = get_object_from_field_name(
                filter_field_name='name',
                filter_field_value=team_name,
                view_url='team'
                )

            if team is None:
                print(ERROR_MESSAGE['team_not_existing'])
                return

            result = self.team_delete(team_id=team['id'])

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result("Impossible de supprimer cette équipe")
            else:
                print_command_result(f"'{team_name}' supprimé avec succès.")

        elif options['update']:
            team_name = input("Nom de l'équipe à modifier: ")
            team_data = get_object_from_field_name(
                filter_field_name='name',
                filter_field_value=team_name,
                view_url='team'
                )

            if team_data is None:
                print(ERROR_MESSAGE['team_not_existing'])
                return

            team_description = TEAM_DESCRIPTION
            print('Entrer les valeurs à mettre à jour, laisser vide pour garder les existantes:')

            for line in TEAM_FIELD_LIST:
                team_description[line] = team_description[line].replace(
                    ':',f' ({team_data[line]}):')

                team_input = input(team_description[line])

                # modify the stored value only if user entered something for this line
                if team_input != "" and team_data[line] != team_input:
                    # getting contract & ee_contact id from user's input
                    team_data[line] = team_input

            result = self.team_update(
                team_id=team_data['id'], team_data=team_data)

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result("Impossible de modifier cette équipe")
            else:
                print_command_result(f"'{team_name}' modifié avec succès.")

    def team_list(self):
        """
        handles 'listing teams
        returns a list of team or None
        '"""
        response = request_commands(view_url='team', operation="read")
        response_data = response.pop(-1)
        if response_data['response_status'] != 200 :
            return None

        team_list = []
        for team_data in response:
            team_list.append(team_data['name'])

        return team_list

    def team_read(self, team_id):
        """
        handles reading one team
        returns dict if found or none if not found
        """
        return request_commands(view_url='team', operation="read", object_id=team_id)

    def team_create(self, team_data):
        """handles creating a new team"""
        return request_commands(view_url='team', operation="create", request_data=team_data)

    def team_delete(self, team_id):
        """handles deleting one team"""
        return request_commands(view_url='team', operation="delete", object_id=team_id)

    def team_update(self, team_id, team_data):
        """handles updating one team"""
        return request_commands(view_url='team', operation="update", request_data=team_data, object_id=team_id)
