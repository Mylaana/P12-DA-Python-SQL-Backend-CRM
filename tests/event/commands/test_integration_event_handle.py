from Event.models import Event
from Event.management.commands import event
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input, setup_session
import time
from EpicEvents.utils import get_object_field_from_id, get_object_from_any_field
import json
import getpass


TEST_EVENT = {
    'name': "test_event",
    'ee_contact': "setup_user",
    'date_start': "2050-01-01T00:00:00Z",
    'date_end': "2050-01-01T23:59:00Z",
    'location': "test_location",
    'attendees': "10",
    'notes': "some notes",
    'contract': "setup_contract",
    'date_start_year': "2050",
    'date_start_month': "01",
    'date_start_day': "01",
    'date_start_hour': "00",
    'date_start_minute': "00",
    'date_end_year': "2050",
    'date_end_month': "01",
    'date_end_day': "01",
    'date_end_hour': "05",
    'date_end_minute': "00",
}

def test_handle_create_should_create_event(capfd, simulate_user_input):
    simulate_user_input([
        TEST_EVENT['name'],
        TEST_EVENT['ee_contact'],
        TEST_EVENT['date_start_year'],
        TEST_EVENT['date_start_month'],
        TEST_EVENT['date_start_day'],
        TEST_EVENT['date_start_hour'],
        TEST_EVENT['date_start_minute'],
        TEST_EVENT['date_end_year'],
        TEST_EVENT['date_end_month'],
        TEST_EVENT['date_end_day'],
        TEST_EVENT['date_end_hour'],
        TEST_EVENT['date_end_minute'],
        TEST_EVENT['location'],
        TEST_EVENT['attendees'],
        TEST_EVENT['notes'],
        TEST_EVENT['contract'],
    ])

    call_command('event', '-create')
    out, err = capfd.readouterr()
    print(out)
    assert str(TEST_EVENT['name']) in str(out)

def test_handle_list_should_print_list(capfd):
    call_command('event', '-list')
    out, err = capfd.readouterr()
    expected_result = TEST_EVENT['name']
    assert expected_result in out

def test_handle_read_should_print_event_info(capfd, simulate_user_input):
    simulate_user_input([TEST_EVENT['name']])

    call_command('event', '-read')
    out, err = capfd.readouterr()
    expected_result = TEST_EVENT['name']

    assert expected_result in out

def test_handle_update_should_update_contrac(capfd, simulate_user_input):
    simulate_user_input([
        TEST_EVENT['name'],
        '',
        '',
        '',
        '',
        '2',
        '',
        ''
    ])
    call_command('event', '-update')
    out, err = capfd.readouterr()
    print(out)
    assert f"'{str(TEST_EVENT['name'])}' modifié avec succès" in str(out)

def test_handle_delete_should_delete_event(capfd, simulate_user_input):
    command = event.Command()
    simulate_user_input([TEST_EVENT['name']])

    call_command('event', '-delete')
    out, err = capfd.readouterr()
    expected_result = f"'{TEST_EVENT['name']}' supprimé avec succès"

    assert expected_result in out
