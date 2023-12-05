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


TEST_CONTRACT = {
    'ee_contact': "setup_user",
    'information': "test_contrat",
    'value_total_price': "100",
    'value_rest_to_pay': "50",
    'status_is_active': "True",
    'client': "setup_client",
}


def test_handle_create_should_create_contract(capfd, simulate_user_input):
    simulate_user_input([
        TEST_CONTRACT['ee_contact'],
        TEST_CONTRACT['information'],
        TEST_CONTRACT['value_total_price'],
        TEST_CONTRACT['value_rest_to_pay'],
        TEST_CONTRACT['status_is_active'],
        TEST_CONTRACT['client'],
    ])

    call_command('contract', '-create')
    out, err = capfd.readouterr()
    assert str(TEST_CONTRACT['information']) in str(out)

def test_handle_list_should_print_list(capfd):
    call_command('contract', '-list')
    out, err = capfd.readouterr()
    expected_result = TEST_CONTRACT['information']
    assert expected_result in out

def test_handle_read_should_print_contract_info(capfd, simulate_user_input):
    simulate_user_input([TEST_CONTRACT['information']])

    call_command('contract', '-read')
    out, err = capfd.readouterr()
    expected_result = TEST_CONTRACT['information']

    assert expected_result in out

def test_handle_update_should_update_contract(capfd, simulate_user_input):
    simulate_user_input([
        TEST_CONTRACT['information'],
        '',
        '',
        '',
        '0',
        '',
        ''
    ])
    call_command('contract', '-update')
    out, err = capfd.readouterr()
    print(out)
    assert f"'{str(TEST_CONTRACT['information'])}' modifié avec succès" in str(out)

def test_handle_delete_should_delete_contract(capfd, simulate_user_input):
    command = contract.Command()
    simulate_user_input([TEST_CONTRACT['information']])

    call_command('contract', '-delete')
    out, err = capfd.readouterr()
    expected_result = f"'{TEST_CONTRACT['information']}' supprimé avec succès"

    assert expected_result in out
