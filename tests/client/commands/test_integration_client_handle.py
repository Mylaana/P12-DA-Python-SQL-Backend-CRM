from Client.models import Client
from Client.management.commands import client
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input
import time
from EpicEvents.utils import get_object_field_from_id, get_object_from_any_field
import json
import getpass


TEST_CLIENT = {
    'name': 'test_client',
    'siren': 'siren000',
    'email': 'email@client.com',
    'phone': '0000',
    'client_contact_name': 'contact',
    'information': 'info000',
    'ee_contact': 1,
    }

def test_handle_create_should_create(simulate_user_input):
    simulate_user_input([
        'admin-oc',
        TEST_CLIENT['name'],
        TEST_CLIENT['siren'],
        TEST_CLIENT['client_contact_name'],
        TEST_CLIENT['email'],
        TEST_CLIENT['phone'],
        TEST_CLIENT['information'],
    ])
    client_object = get_object_from_any_field(
        view_url='client',
        filter_field_name='name',
        filter_field_value=TEST_CLIENT['name'])
    assert client_object is None

    call_command('client', '-create')

    client_object = get_object_from_any_field(
        view_url='client',
        filter_field_name='name',
        filter_field_value=TEST_CLIENT['name'])
    assert client_object is not None

def test_handle_list_should_print_list(capfd):
    call_command('client', '-list')
    out, err = capfd.readouterr()
    expected_result = TEST_CLIENT['name']

    assert expected_result in out

def test_handle_read_should_print_client_info(capfd, simulate_user_input):
    command = client.Command()
    simulate_user_input(['test_client'])

    call_command('client', '-read')
    out, err = capfd.readouterr()
    expected_result = TEST_CLIENT['name']

    assert expected_result in out

def test_handle_update_should_update(simulate_user_input):
    updated_siren = 'siren111'
    simulate_user_input([
        'test_client',
        '',
        '',
        updated_siren,
        '',
        '',
        '',
        '',
    ])

    call_command('client', '-update')

    client_object = get_object_from_any_field(
        view_url='client',
        filter_field_name='name',
        filter_field_value=TEST_CLIENT['name'])
    assert client_object is not None
    assert str(client_object['siren']) == str(updated_siren)

def test_handle_delete_should_delete_client(capfd, simulate_user_input):
    command = client.Command()
    simulate_user_input(['test_client'])

    call_command('client', '-delete')
    out, err = capfd.readouterr()
    expected_result = f"'{TEST_CLIENT['name']}' supprimé avec succès"

    assert expected_result in out
