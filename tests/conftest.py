import pytest
from Client.models import Client
from Contract.models import Contract
from Contract.management.commands import contract
from Client.management.commands import client
from UserProfile.management.commands import user, team
from UserProfile.models import UserProfile, Team
from Event.management.commands import event
from Event.models import Event

SETUP_TEAM_FIELDS = {
    'name': 'setup_team'
}

SETUP_USER_FIELDS = {
    'username': 'setup_user',
    'password': 'setup_password123$A',
    'team': '',
    'email': 'setup_user@ee.com',
    'first_name': 'test user prenom',
    'last_name': 'test user nom',
    'phone': '0000000000'
    }

SETUP_CLIENT_FIELDS = {
    'name': 'setup_client',
    'siren': 'setup_siren',
    'email': 'setup_client@client.com',
    'phone': 'setup_phone',
    'client_contact_name': 'contact',
    'information': 'setup_info',
    'ee_contact': '',
    }

SETUP_CONTRACT_FIELDS = {
    'ee_contact': '',
    'information': 'setup_contract',
    'value_total_price': '100',
    'value_rest_to_pay': '50',
    'status_is_active': 'True',
    'client': '',
}


@pytest.fixture(scope='session', autouse=True)
def setup_session():
    # Setup
    team_command = team.Command()
    setup_team = team_command.team_create(SETUP_TEAM_FIELDS)[0]

    setup_user_fields = SETUP_USER_FIELDS
    setup_user_fields['team'] = setup_team['id']
    user_command = user.Command()
    setup_user = user_command.user_create(setup_user_fields)[0]

    setup_client_fields = SETUP_CLIENT_FIELDS
    setup_client_fields['ee_contact'] = setup_user['id']
    client_command = client.Command()
    setup_client = client_command.client_create(setup_client_fields)[0]

    setup_contract_fields = SETUP_CONTRACT_FIELDS
    setup_contract_fields['ee_contact'] = setup_user['id']
    setup_contract_fields['client'] = setup_client['id']
    contract_command = contract.Command()
    setup_contract = contract_command.contract_create(setup_contract_fields)[0]

    yield

    # Teardown
    team_command.team_delete(setup_team['id'])
    user_command.user_delete(setup_user['id'])
    client_command.client_delete(setup_client['id'])

    #should already be deleted by on_delete=Cascade
    contract_command.contract_delete(setup_contract['id'])
    # event_command.event_delete(setup_event['id'])
