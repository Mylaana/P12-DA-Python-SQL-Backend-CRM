from UserProfile.models import UserProfile, Team
from UserProfile.management.commands import user
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input
import time
from EpicEvents.utils import get_object_field_from_id, get_object_from_any_field
import json
import getpass


TEST_USER = {'username': 'test_user',
             'password': 'test_password123$A',
             'team': '1',
             'email': 'test_user@ee.com',
             'first_name': 'test user prenom',
             'last_name': 'test user nom',
             'phone': '0000000000'}

@patch('UserProfile.management.commands.user.getpass', Mock(return_value='test_password123$A'))
def test_handle_create_should_create_user(capfd, simulate_user_input):
    simulate_user_input([
        'test_user',
        'gestion',
        'test_user@ee.com',
        'test user prenom',
        'test user nom',
        '0000000000'
    ])
    call_command('user', '-create')
    out, err = capfd.readouterr()
    assert str(TEST_USER['username']) in str(out)

def test_handle_list_should_print_list(capfd):
    call_command('user', '-list')
    out, err = capfd.readouterr()
    expected_result = TEST_USER['username']
    assert expected_result in out

def test_handle_read_should_print_user_info(capfd, simulate_user_input):
    command = user.Command()
    simulate_user_input(['test_user'])

    call_command('user', '-read')
    out, err = capfd.readouterr()
    expected_result = TEST_USER['username']

    assert expected_result in out

@patch('UserProfile.management.commands.user.getpass', Mock(return_value=''))
def test_handle_update_should_update_user(capfd, simulate_user_input):
    simulate_user_input([
        'test_user',
        '',
        '',
        '',
        '',
        '',
        'phone111'
    ])
    call_command('user', '-update')
    out, err = capfd.readouterr()
    print(out)
    assert str(TEST_USER['username']) in str(out)

def test_handle_delete_should_delete_user(capfd, simulate_user_input):
    command = user.Command()
    simulate_user_input(['test_user'])

    call_command('user', '-delete')
    out, err = capfd.readouterr()
    expected_result = f"'{TEST_USER['username']}' supprimé avec succès"

    assert expected_result in out
