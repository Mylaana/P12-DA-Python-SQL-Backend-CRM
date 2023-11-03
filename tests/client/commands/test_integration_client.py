from Client.management.commands import client
import pytest
from unittest.mock import patch
"""
@pytest.mark.django_db
def test_should_return_user_id():
    command = client.Command()

    username = "admin-oc"
    user_id = command.get_ee_contact_id(username)

    assert isinstance(user_id, int)

@pytest.mark.django_db
@patch('Client.management.commands.client.Command.client_list.response', new_callable=lambda: [1, 2, 3])
def test_should_return_client_list():
    command = client.Command()

    client_list = command.client_list()

    assert client_list is not None

"""