from Client.models import Client
from Client.management.commands import client
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input
import time
from EpicEvents.utils import get_object_field_from_id, get_object_from_any_field
import json


TEST_CLIENT = {
    'name': 'test_client',
    'siren': 'siren000',
    'email': 'email@client.com',
    'phone': '0000',
    'client_contact_name': 'contact',
    'information': 'info000',
    'ee_contact': 1,
    }


@pytest.mark.django_db
def test_client_create_should_create():
    command = client.Command()
    returned_value = command.client_create(TEST_CLIENT)
    assert TEST_CLIENT['name'] == returned_value[0]['name']

    client_id = get_object_from_any_field(
        view_url='client',
        filter_field_name='name',
        filter_field_value=TEST_CLIENT['name'])
    assert client_id is not None

@pytest.mark.django_db
def test_client_list_should_return_list():
    command = client.Command()
    returned_value = command.client_list()

    assert TEST_CLIENT['name'] in returned_value


@pytest.mark.django_db
def test_client_update_should_update():
    command = client.Command()
    client_object = get_object_from_any_field(
        view_url='client',
        filter_field_name='name',
        filter_field_value=TEST_CLIENT['name'])

    client_id = client_object['id']
    assert client_id is not None

    test_client = TEST_CLIENT
    test_client['siren'] = 'siren111'
    returned_value = command.client_update(client_id=client_id, client_data=test_client)
    assert returned_value[-1]['operation'] == 'update'
    assert str(returned_value[0]['siren']) == 'siren111'

@pytest.mark.django_db
def test_client_delete_should_delete():
    command = client.Command()
    client_object = get_object_from_any_field(
        view_url='client',
        filter_field_name='name',
        filter_field_value=TEST_CLIENT['name'])

    client_id = client_object['id']
    assert client_id is not None

    returned_value = command.client_delete(client_id=client_id)
    assert returned_value[-1]['operation'] == 'delete'
