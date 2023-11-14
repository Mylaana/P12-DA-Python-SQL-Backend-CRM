from datetime import datetime
from django.core.management.base import BaseCommand
from UserProfile.models import UserProfile
from EpicEvents.utils import input_validated, request_commands, print_command_result
from EpicEvents.utils import get_team_id, get_ee_contact_id


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
            team_id = get_team_id(name=team_name)
            if team_id is None:
                print_command_result("Impossible de trouver cet équipe.")
                return

            result = self.team_read(team_id=team_id)

            team_info = []
            for line in TEAM_FIELD_LIST:
                team_info.append(f"{TEAM_DESCRIPTION[line]} {result[line]}")

            print_command_result(printable=team_info)

            return

        elif options['create']:
            team_data = {
            }

            # gets team's info from team's input
            for line in TEAM_FIELD_LIST:
                team_input = input(TEAM_DESCRIPTION[line])
                input_valid = input_validated(team_input)
                if not input_valid:
                    return
                team_data[line] = team_input

            result = self.team_create(team_data)

            if result is None:
                print_command_result('Impossible de créer cette équipe.')
            else:
                print_command_result(f"Equipe '{team_data['name']}' créé avec succès")

        elif options['delete']:
            team_name = input("Nom de l'équipe à supprimer: ")
            team_id = get_team_id(name=team_name)

            if team_id is None:
                print("Impossible de trouver cette équipe dans la base de données.")
                return

            result = self.team_delete(team_id=team_id)
            if result is None:
                print_command_result("Impossible de supprimer cette équipe")
            else:
                print_command_result(f"'{team_name}' supprimé avec succès.")

        elif options['update']:
            team_name = input("Nom de l'équipe à modifier: ")
            team_id = get_team_id(name=team_name)

            if team_id is None:
                print("Impossible de trouver cette équipe dans la base de données.")
                return

            # get team data
            team_data = self.team_read(team_id)
            team_description = TEAM_DESCRIPTION
            print('Entrer les valeurs à mettre à jour, laisser vide pour garder les existantes:')
            for line in TEAM_FIELD_LIST:
                team_description[line] = team_description[line].replace(':',f' ({team_data[line]}):' )
                team_input = input(team_description[line])

                # modify the stored value only if team entered something
                if team_input != "":
                    team_data[line] = team_input

            result = self.team_update(team_id=team_id, team_data=team_data)
            if result is None:
                print_command_result("Impossible de modifier ce team")
            else:
                print_command_result(f"'{team_name}' modifié avec succès.")


    def team_list(self):
        """
        handles 'listing teams
        returns a list of team or None
        '"""
        response = request_commands(view_url='team', operation="read")
        if response is None:
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
