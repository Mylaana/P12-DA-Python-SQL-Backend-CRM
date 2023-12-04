from Contract.models import Contract
from Contract.management.commands import contract
from Client.management.commands import client
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input, setup_session, SETUP_CLIENT_FIELDS
import time
from EpicEvents.utils import get_object_field_from_id, get_object_from_any_field
import json


TEST_CONTRACT = {
    'ee_contact': "1",
    'information': "contrat_test",
    'value_total_price': "100",
    'value_rest_to_pay': "50",
    'status_is_active': "True",
    'client': "",
}

@pytest.mark.django_db
def test_contract_create_should_create():
    test_contract = TEST_CONTRACT
    test_contract['ee_contact'] = get_object_from_any_field('user','username','setup_user')['id']
    test_contract['client'] = get_object_from_any_field('client','name','setup_client')['id']
    command = contract.Command()
    returned_value = command.contract_create(test_contract)
    assert TEST_CONTRACT['information'] == returned_value[0]['information']

@pytest.mark.django_db
def test_contract_list_should_list():
    command = contract.Command()
    returned_value = command.contract_list()
    assert TEST_CONTRACT['information'] in returned_value

@pytest.mark.django_db
def test_contract_read_should_return_contract_info():
    command = contract.Command()
    contract_object = get_object_from_any_field(
        view_url='contract',
        filter_field_name='information',
        filter_field_value=TEST_CONTRACT['information']
        )

    returned_value = command.contract_read(contract_id=contract_object['id'])

    assert contract_object is not None
    assert contract_object['information'] == TEST_CONTRACT['information']

@pytest.mark.django_db
def test_contract_update_should_update():
    command = contract.Command()
    contract_object = get_object_from_any_field(
        view_url='contract',
        filter_field_name='information',
        filter_field_value=TEST_CONTRACT['information']
        )

    # asserting test_contract state before update
    assert contract_object is not None
    assert int(contract_object['value_rest_to_pay']) == int(TEST_CONTRACT['value_rest_to_pay'])

    test_contract = TEST_CONTRACT
    test_contract['value_rest_to_pay'] = 0

    returned_value = command.contract_update(contract_id=contract_object['id'], contract_data=test_contract)
    assert int(returned_value[0]['value_rest_to_pay']) == 0
    assert returned_value[-1]['operation'] == 'update'

@pytest.mark.django_db
def test_contract_delete_should_delete():
    command = contract.Command()
    contract_object = get_object_from_any_field(
        view_url='contract',
        filter_field_name='information',
        filter_field_value=TEST_CONTRACT['information']
        )

    # asserting contract is in DB before deleting
    assert contract_object is not None

    returned_value = command.contract_delete(contract_id=contract_object['id'])
    assert returned_value[0]['operation'] == 'delete'
