from Contract.models import Contract
from Contract.management.commands import contract
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input
import time
from EpicEvents.utils import get_object_field_from_id, get_object_from_any_field
import json
import getpass


TEST_TEAM = {
    'name': "test_team",
}


def test_handle_create_should_create_contract(capfd, simulate_user_input):
    simulate_user_input([
        TEST_TEAM['name'],
    ])

    call_command('team', '-create')
    out, err = capfd.readouterr()
    assert str(TEST_TEAM['name']) in str(out)

def test_handle_list_should_print_list(capfd):
    call_command('team', '-list')
    out, err = capfd.readouterr()
    expected_result = TEST_TEAM['name']
    assert expected_result in out

def test_handle_read_should_print_contract_info(capfd, simulate_user_input):
    simulate_user_input([TEST_TEAM['name']])

    call_command('team', '-read')
    out, err = capfd.readouterr()
    expected_result = TEST_TEAM['name']

    assert expected_result in out

def test_handle_update_should_update_contract(capfd, simulate_user_input):
    simulate_user_input([
        TEST_TEAM['name'],
        TEST_TEAM['name'] + '_updated',
    ])
    call_command('team', '-update')
    out, err = capfd.readouterr()

    assert f"modifié avec succès" in str(out)

def test_handle_delete_should_delete_contract(capfd, simulate_user_input):
    command = contract.Command()
    simulate_user_input([TEST_TEAM['name']+'_updated'])

    call_command('team', '-delete')
    out, err = capfd.readouterr()
    expected_result = f"supprimé avec succès"

    assert expected_result in out
