from Client.management.commands import client
import pytest
from unittest.mock import patch, Mock

"""
@pytest.mark.django_db
def test_should_return_user_id():
    command = client.Command()

    username = "admin-oc"
    user_id = command.get_ee_contact_id(username)

    assert isinstance(user_id, int)
"""

TEST_CLIENT_LIST = [{'id': 0, 'name': 'test_client', 'siren': 'siren000',
               'email': 'email@client.com', 'phone': '0000',
               'client_contact_name': 'contact', 'information': 'info000',
               'date_creation': '2023-10-30T10:52:06.993607Z',
               'date_update': '2023-10-31T09:30:42.559786Z', 'ee_contact': 0}]

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


@pytest.mark.django_db
@patch('Client.management.commands.client.request_commands', Mock(return_value=None))
def test_client_read_should_return_None():
    command = client.Command()
    returned_value = command.client_read('test_client')

    assert returned_value is None

@pytest.mark.django_db
@patch('Client.management.commands.client.request_commands', Mock(return_value=TEST_CLIENT_LIST))
@patch('Client.management.commands.client.Command.get_ee_contact_name', Mock(return_value='contact_name'))
def test_client_read_should_return_info():
    command = client.Command()
    returned_value = command.client_read('test_client')
    expected_result = 'Client: test_client'

    assert isinstance(returned_value, list)
    assert expected_result in returned_value[0]


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
