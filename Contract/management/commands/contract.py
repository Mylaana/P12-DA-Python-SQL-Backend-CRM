from datetime import datetime
from django.core.management.base import BaseCommand
from Contract.models import Contract
from EpicEvents.utils import input_validated, request_commands, print_command_result
from EpicEvents.utils import get_object_from_field_name
from getpass import getpass


CONTRACT_FIELD_LIST = [
    'ee_contact',
    'information',
    'value_total_price',
    'value_rest_to_pay',
    'status_is_active',
    'client',
    ]


CONTRACT_DESCRIPTION = {
    'ee_contact': "Nom du contact EpicEvents: ",
    'information': "Information: ",
    'value_total_price': "Montant total contractualisé: ",
    'value_rest_to_pay': "Reste à payer: ",
    'status_is_active': "Contract actif: ",
    'client': "Nom du client: ",
}

class Command(BaseCommand):
    """create contract command"""

    help = 'Commande personnalisée pour effectuer des opérations liées aux contrats'

    def add_arguments(self, parser):
        """parsing arguments passed to contract command"""
        parser.add_argument('-list', '--list', action='store_true', help='Liste les instances de contract')
        parser.add_argument('-read', '--read', action='store_true', help='Lis une instance de contract')
        parser.add_argument('-create', '--create', action='store_true', help='Crée une instance de contract')
        parser.add_argument('-delete', '--delete', action='store_true', help='Supprime une instance de contract')
        parser.add_argument('-update', '--update', action='store_true', help='Mets à jour une instance de contract')

    def handle(self, *args, **options):
        """handles 'contracts related commands'"""
        if options['list']:
            result = self.contract_list()
            if result is None:
                print_command_result("Aucun contrat trouvé dans la base de donnée")
            else:
                print_command_result("liste des contrats :", result)

        elif options['read']:
            contract_name = input("Information du contrat: ")
            contract = get_object_from_field_name(
                view_url='contract',
                filter_field_name='information',
                filter_field_value=contract_name,
                )

            if contract is None:
                print_command_result("Impossible de trouver cet contrat.")
                return

            # formatting contract for terminal output
            contract_info = []
            for line in CONTRACT_FIELD_LIST:
                contract_info.append(f"{CONTRACT_DESCRIPTION[line]} {contract[line]}")

            print_command_result(printable=contract_info)

            return

        elif options['create']:
            contract_field_list_create = CONTRACT_FIELD_LIST

            # gets contract's info from user's input
            contract_data = {}
            for line in contract_field_list_create:
                if line == 'client':
                    client = get_object_from_field_name(
                        filter_field_name='name',
                        filter_field_value=input(CONTRACT_DESCRIPTION[line]),
                        view_url='client'
                        )
                    contract_input = client['id']
                elif line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='username',
                        filter_field_value=input(CONTRACT_DESCRIPTION[line]),
                        view_url='user'
                    )
                    contract_input = user['id']
                else:
                    contract_input = input(CONTRACT_DESCRIPTION[line])

                input_valid = input_validated(contract_input)
                if not input_valid:
                    return
                contract_data[line] = contract_input
            print(contract_data)
            result = self.contract_create(contract_data)

            if result is None:
                print_command_result('Impossible de créer cet contrat.')
            else:
                print_command_result(f"Contrat '{contract_data['information']}' créé avec succès")

        elif options['delete']:
            contract_name = input("Nom du contrat à supprimer: ")
            contract_id = get_ee_contract_id(name=contract_name)

            if contract_id is None:
                print("Impossible de trouver cet contrat dans la base de données.")
                return

            result = self.contract_delete(contract_id=contract_id)
            if result is None:
                print_command_result("Impossible de supprimer ce user")
            else:
                print_command_result(f"'{contract_name}' supprimé avec succès.")

        elif options['update']:
            contract_name = input("Nom du contrat à modifier: ")
            contract_id = get_ee_contract_id(name=contract_name)

            if contract_id is None:
                print("Impossible de trouver cet contrat dans la base de données.")
                return

            # get user data
            contract_data = self.contract_read(contract_id)
            contract_description = CONTRACT_DESCRIPTION
            print('Entrer les valeurs à mettre à jour, laisser vide pour garder les existantes:')
            print(CONTRACT_FIELD_LIST_UNSAFE)
            print(contract_description)
            for line in CONTRACT_FIELD_LIST_UNSAFE:
                if line == 'team':
                    contract_description[line] = contract_description[line].replace(
                        ':',f' ({get_team_name(contract_data[line])}):')
                else:
                    contract_description[line] = contract_description[line].replace(
                        ':',f' ({contract_data[line]}):')

                if line == 'password':
                    contract_input = getpass(contract_description[line])
                else:
                    contract_input = input(contract_description[line])

                # modify the stored value only if contract entered something
                if contract_input != "":
                    contract_data[line] = contract_input

            result = self.contract_update(contract_id=contract_id, contract_data=contract_data)
            if result is None:
                print_command_result("Impossible de modifier ce contrat")
            else:
                print_command_result(f"'{contract_name}' modifié avec succès.")


    def contract_list(self):
        """
        handles 'listing contracts
        returns a list of contract or None
        '"""
        response = request_commands(view_url='contract', operation="read")
        if response is None:
            return None

        contract_list = []
        for contract_data in response:
            contract_list.append(contract_data['information'])

        return contract_list

    def contract_read(self, contract_id:int):
        """
        handles reading one contract
        returns dict if found or none if not found
        """
        return request_commands(view_url='contract', operation="read", object_id=contract_id)

    def contract_create(self, contract_data:dict):
        """handles creating a new contract
        gets a dict for contract data
        returns 'create if successful'
        """
        return request_commands(view_url='contract', operation="create", request_data=contract_data)

    def contract_delete(self, contract_id:int):
        """handles deleting one contract
        gets contract id (integer)
        returns 'delete' if successful
        """
        return request_commands(view_url='contract', operation="delete", object_id=contract_id)

    def contract_update(self, contract_id:int, contract_data:dict):
        """handles updating one contract
        gets contract id (integer)
        returns 'update' if successful
        """
        return request_commands(view_url='contract', operation="update", request_data=contract_data, object_id=contract_id)
