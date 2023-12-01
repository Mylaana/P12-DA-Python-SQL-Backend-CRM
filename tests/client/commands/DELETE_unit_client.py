from Client.management.commands import client
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input


TEST_CLIENT_INFO = {
    'id': 0,
    'name': 'test_client',
    'siren': 'siren000',
    'email': 'email@client.com',
    'phone': '0000',
    'client_contact_name': 'contact',
    'information': 'info000',
    'date_creation': '2023-10-30T10:52:06.993607Z',
    'date_update': '2023-10-31T09:30:42.559786Z',
    'ee_contact': 0,
    'ee_contact_name': 'ee_contact_name',
    'ee_contact_id': 0
    }

TEST_CLIENT_LIST = [TEST_CLIENT_INFO]

# Test client_list method
@pytest.mark.django_db
@patch('Client.management.commands.client.request_commands', Mock(return_value=None))
def test_client_list_should_return_None():
    command = client.Command()
    returned_value = command.client_list()

    assert returned_value is None

@pytest.mark.django_db
@patch('Client.management.commands.client.request_commands', Mock(return_value=TEST_CLIENT_LIST))
def test_client_list_should_return_list():
    command = client.Command()
    returned_value = command.client_list()
    expected_result = ['test_client']

    assert isinstance(returned_value, list)
    assert returned_value == expected_result

# Test client_read method
@pytest.mark.django_db
@patch('Client.management.commands.client.request_commands', Mock(return_value=TEST_CLIENT_INFO))
@patch('Client.management.commands.client.get_ee_contact_name', Mock(return_value='contact_name'))
def test_client_read_should_return_info():
    command = client.Command()
    returned_value = command.client_read(0)
    expected_result = 'name'

    assert isinstance(returned_value, dict)
    assert expected_result in returned_value

# Test client_delete method
@pytest.mark.django_db
@patch('Client.management.commands.client.request_commands', Mock(return_value=None))
def test_client_delete_should_return_None():
    command = client.Command()
    returned_value = command.client_delete('test_client')

    assert returned_value is None

@pytest.mark.django_db
@patch('Client.management.commands.client.request_commands', Mock(return_value='delete'))
def test_client_delete_should_return_confirmation():
    command = client.Command()
    returned_value = command.client_delete('test_client')
    expected_result = 'delete'

    assert expected_result == returned_value

# Test client_update method
@pytest.mark.django_db
@patch('Client.management.commands.client.request_commands', Mock(return_value=None))
def test_client_update_should_return_None():
    command = client.Command()
    returned_value = command.client_delete('test_client')

    assert returned_value is None

@pytest.mark.django_db
@patch('Client.management.commands.client.request_commands', Mock(return_value='update'))
def test_client_update_should_return_confirmation():
    command = client.Command()
    returned_value = command.client_delete('test_client')
    expected_result = 'update'

    assert expected_result == returned_value

# Test List command handler
@patch('Client.management.commands.client.Command.client_list', Mock(return_value=None))
def test_handle_list_should_print_not_found(capfd):
    call_command('client', '-list')
    out, err = capfd.readouterr()
    expected_result = "Aucun client trouvé dans la base de donnée"
    assert expected_result.strip().lower() == out.strip().lower()

@patch('Client.management.commands.client.Command.client_list', Mock(return_value=TEST_CLIENT_LIST))
def test_handle_list_should_print_list(capfd):
    call_command('client', '-list')
    out, err = capfd.readouterr()
    expected_result = "test_client"
    assert expected_result in out

# Test Read command handler
@patch('Client.management.commands.client.get_ee_client_id', Mock(return_value=None))
def test_handle_read_should_print_not_found(capfd, simulate_user_input):
    simulate_user_input(["client_name_not_existing"])

    call_command('client', '-read')
    out, err = capfd.readouterr()
    expected_result = "Impossible de trouver ce client"

    assert out.strip().lower() == expected_result.strip().lower()


@patch('Client.management.commands.client.Command.client_read', Mock(return_value=TEST_CLIENT_INFO))
@patch('Client.management.commands.client.get_ee_client_id', Mock(return_value=0))
def test_handle_read_should_print_client(capfd, simulate_user_input):
    simulate_user_input(["test_client"])

    call_command('client', '-read')
    out, err = capfd.readouterr()

    assert "test_client" in out
    assert "email@client.com" in out

# Test Create command handler
@patch('Client.management.commands.client.get_ee_contact_id', Mock(return_value=None))
def test_handle_create_should_print_user_not_found(capfd, simulate_user_input):
    simulate_user_input(["user_name_not_existing"])

    call_command('client', '-create')
    out, err = capfd.readouterr()
    expected_result = "Impossible de trouver cet utilisateur"

    assert expected_result.strip().lower() in out.strip().lower()
    assert isinstance(out, str)

@pytest.mark.django_db
@patch('Client.management.commands.client.Command.client_create', Mock(return_value=None))
@patch('Client.management.commands.client.get_ee_contact_id', Mock(return_value=0))
def test_handle_create_should_print_error_creating_client(capfd, simulate_user_input):
    simulate_user_input([
        'ee_contact_name',
        'test_client',
        'siren000',
        'contact',
        'email@client.com',
        '0000',
        'info000'
        ])

    call_command('client', '-create')
    out, err = capfd.readouterr()
    expected_value = "impossible de créer ce client."
    assert expected_value.strip().lower() in out.strip().lower()

@pytest.mark.django_db
@patch('Client.management.commands.client.Command.client_create', Mock(return_value='create'))
@patch('Client.management.commands.client.get_ee_contact_id', Mock(return_value=0))
def test_handle_create_should_print_client_created(capfd, simulate_user_input):
    simulate_user_input([
        'ee_contact_name',
        'test_client',
        'siren000',
        'contact',
        'email@client.com',
        '0000',
        'info000'
        ])

    call_command('client', '-create')
    out, err = capfd.readouterr()
    expected_value = "Client 'test_client' créé avec succès"
    assert expected_value.strip().lower() in out.strip().lower()

# Test Delete command handler
@patch('Client.management.commands.client.get_ee_client_id', Mock(return_value=None))
def test_handle_delete_should_print_client_not_found(capfd, simulate_user_input):
    simulate_user_input(["client_name_not_existing"])

    call_command('client', '-delete')
    out, err = capfd.readouterr()
    expected_result = "Impossible de trouver ce client dans la base de données."

    assert expected_result.strip().lower() in out.strip().lower()
    assert isinstance(out, str)


@pytest.mark.django_db
@patch('Client.management.commands.client.Command.client_delete', Mock(return_value=None))
@patch('Client.management.commands.client.get_ee_client_id', Mock(return_value=0))
def test_handle_delete_should_print_error_deleting_client(capfd, simulate_user_input):
    simulate_user_input(["client_name_not_existing"])

    call_command('client', '-delete')
    out, err = capfd.readouterr()
    expected_value = "impossible de supprimer ce client"
    assert expected_value.strip().lower() in out.strip().lower()

@pytest.mark.django_db
@patch('Client.management.commands.client.Command.client_delete', Mock(return_value='delete'))
@patch('Client.management.commands.client.get_ee_client_id', Mock(return_value=0))
def test_handle_delete_should_print_client_deleted(capfd, simulate_user_input):
    simulate_user_input(["test_client"])

    call_command('client', '-delete')
    out, err = capfd.readouterr()
    expected_value = "'test_client' supprimé avec succès"

    assert expected_value.strip().lower() in out.strip().lower()


# Test Update command handler
@patch('Client.management.commands.client.get_ee_client_id', Mock(return_value=None))
def test_handle_update_should_print_client_not_found(capfd, simulate_user_input):
    simulate_user_input(["client_name_not_existing"])

    call_command('client', '-update')
    out, err = capfd.readouterr()
    expected_result = "impossible de trouver ce client dans la base de données"

    assert expected_result.strip().lower() in out.strip().lower()
    assert isinstance(out, str)

@pytest.mark.django_db
@patch('Client.management.commands.client.Command.client_read', Mock(return_value=TEST_CLIENT_INFO))
@patch('Client.management.commands.client.Command.client_update', Mock(return_value=None))
@patch('Client.management.commands.client.get_ee_client_id', Mock(return_value=0))
def test_handle_update_should_print_error_creating_client(capfd, simulate_user_input):
    simulate_user_input(['client_name_not_existing'] + [''] * 7)

    call_command('client', '-update')
    out, err = capfd.readouterr()
    expected_value = "Impossible de modifier ce client"
    print(out)
    assert expected_value.strip().lower() in out.strip().lower()

@pytest.mark.django_db
@patch('Client.management.commands.client.Command.client_read', Mock(return_value=TEST_CLIENT_INFO))
@patch('Client.management.commands.client.Command.client_update', Mock(return_value='update'))
@patch('Client.management.commands.client.get_ee_client_id', Mock(return_value=0))
def test_handle_update_should_print_client_created(capfd, simulate_user_input):
    simulate_user_input(['client_name_not_existing'] + [''] * 7)

    call_command('client', '-update')
    out, err = capfd.readouterr()
    expected_value = "'client_name_not_existing' modifié avec succès."
    assert expected_value.strip().lower() in out.strip().lower()
