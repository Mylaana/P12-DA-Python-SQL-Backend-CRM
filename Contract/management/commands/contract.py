from datetime import datetime
from django.core.management.base import BaseCommand
from Contract.models import Contract
from EpicEvents.utils import input_validated, request_commands, print_command_result
from EpicEvents.utils import get_object_from_field_name
from EpicEvents.utils import ERROR_MESSAGE
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
        parser.add_argument('-own', '--own', action='store_true', help='filtre la liste sur les contrats qui vous sont attribués')
        parser.add_argument('-read', '--read', action='store_true', help='Lis une instance de contract')
        parser.add_argument('-create', '--create', action='store_true', help='Crée une instance de contract')
        parser.add_argument('-delete', '--delete', action='store_true', help='Supprime une instance de contract')
        parser.add_argument('-update', '--update', action='store_true', help='Mets à jour une instance de contract')

    def handle(self, *args, **options):
        """handles 'contracts related commands'"""
        if options['list']:
            result = self.contract_list(options['own'])
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
                print_command_result(ERROR_MESSAGE['contract_not_existing'])
                return

            # formatting contract for terminal output
            contract_info = []
            for line in CONTRACT_FIELD_LIST:
                if line == 'client':
                    client = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=contract['client'],
                        view_url='client'
                    )
                    contract_info.append(f"{CONTRACT_DESCRIPTION[line]} {client['name']}")
                elif line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=contract['ee_contact'],
                        view_url='user'
                    )
                    contract_info.append(f"{CONTRACT_DESCRIPTION[line]} {user['username']}")
                else:
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
                    if client is None:
                        print(ERROR_MESSAGE['client_not_existing'])
                        return None
                    contract_input = client['id']
                elif line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='username',
                        filter_field_value=input(CONTRACT_DESCRIPTION[line]),
                        view_url='user'
                    )
                    if  user is None:
                        print(ERROR_MESSAGE['user_not_existing'])
                        return None
                    contract_input = user['id']
                else:
                    contract_input = input(CONTRACT_DESCRIPTION[line])

                input_valid = input_validated(contract_input)
                if not input_valid:
                    return
                contract_data[line] = contract_input

            result = self.contract_create(contract_data)

            if result[-1]['response_status'] // 100 != 2 :
                print_command_result('Impossible de créer cet contrat.')
                print(result[-1]['response_text'])
            else:
                print_command_result(f"Contrat '{contract_data['information']}' créé avec succès")

        elif options['delete']:
            contract_name = input("Information du contrat à supprimer: ")
            contract = get_object_from_field_name(
                filter_field_name='information',
                filter_field_value=contract_name,
                view_url='contract'
                )

            if contract is None:
                print(ERROR_MESSAGE['contract_not_existing'])
                return

            result = self.contract_delete(contract_id=contract['id'])
            if result[-1]['response_status'] // 100 != 2 :
                print_command_result("Impossible de supprimer ce contrat")
            else:
                print_command_result(f"'{contract_name}' supprimé avec succès.")

        elif options['update']:
            contract_name = input("Information du contrat à modifier: ")
            contract_data = get_object_from_field_name(
                filter_field_name='information',
                filter_field_value=contract_name,
                view_url='contract'
                )

            if contract_data is None:
                print(ERROR_MESSAGE['contract_not_existing'])
                return

            contract_description = CONTRACT_DESCRIPTION
            print('Entrer les valeurs à mettre à jour, laisser vide pour garder les existantes:')

            for line in CONTRACT_FIELD_LIST:
                if line == 'client':
                    client = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=contract_data['client'],
                        view_url='client'
                        )
                    contract_description[line] = contract_description[line].replace(
                        ':',f" ({client['name']}):")
                elif line == 'ee_contact':
                    user = get_object_from_field_name(
                        filter_field_name='id',
                        filter_field_value=contract_data['ee_contact'],
                        view_url='user'
                    )
                    contract_description[line] = contract_description[line].replace(
                        ':',f" ({user['username']}):")
                else:
                    contract_description[line] = contract_description[line].replace(
                        ':',f' ({contract_data[line]}):')

                contract_input = input(contract_description[line])

                # modify the stored value only if user entered something for this line
                if contract_input != "" and contract_data[line] != contract_input:
                    # getting client & ee_contact id from user's input
                    if line == 'client':
                        client = get_object_from_field_name(
                            filter_field_name='name',
                            filter_field_value=contract_input,
                            view_url='client'
                            )
                        if client is None:
                            print_command_result(ERROR_MESSAGE['client_not_existing'])
                            return
                        contract_data[line] = client['id']
                    elif line == 'ee_contact':
                        user = get_object_from_field_name(
                            filter_field_name='username',
                            filter_field_value=contract_input,
                            view_url='user'
                        )
                        if user is None:
                            print_command_result(ERROR_MESSAGE['user_not_existing'])
                            return
                        contract_data[line] = user['id']
                    else:
                        contract_data[line] = contract_input

            result = self.contract_update(
                contract_id=contract_data['id'], contract_data=contract_data)
            if result[-1]['response_status'] // 100 != 2 :
                print_command_result("Impossible de modifier ce contrat")
            else:
                print_command_result(f"'{contract_name}' modifié avec succès.")

    def contract_list(self, own:bool=False):
        """
        handles 'listing contracts
        returns a list of contract or None
        '"""
        response = request_commands(view_url='contract', operation="read")
        response_data = response.pop(-1)
        if response_data['response_status'] // 100 != 2 :
            return None

        contract_list = []
        for contract_data in response:
            if contract_data['epicevents_contact_name'] == response_data['request_username'] or own == False:
                contract_list.append(contract_data['information'])

        if contract_list == []:
            contract_list = None

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
