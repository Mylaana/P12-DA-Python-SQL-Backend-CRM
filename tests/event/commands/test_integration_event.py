from Event.models import Event
from Event.management.commands import event
from Client.management.commands import client
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input, setup_session, SETUP_CLIENT_FIELDS
import time
from EpicEvents.utils import get_object_field_from_id, get_object_from_any_field
import json


TEST_EVENT = {
    'ee_contact': "",
    'contract': "",
    'name': "test_event",
    'date_start': "2050-01-01T00:00:00Z",
    'date_end': "2050-01-01T23:59:00Z",
    'location': "test_location",
    'attendees': "10",
    'notes': "some notes",
}

@pytest.mark.django_db
def test_event_create_should_create():
    test_event = TEST_EVENT
    test_event['ee_contact'] = get_object_from_any_field('user','username','setup_user')['id']
    test_event['contract'] = get_object_from_any_field('contract','information','setup_contract')['id']
    command = event.Command()
    returned_value = command.event_create(test_event)
    assert TEST_EVENT['name'] == returned_value[0]['name']

@pytest.mark.django_db
def test_event_list_should_list():
    command = event.Command()
    returned_value = command.event_list()
    assert TEST_EVENT['name'] in returned_value

@pytest.mark.django_db
def test_event_update_should_update():
    command = event.Command()
    event_object = get_object_from_any_field(
        view_url='event',
        filter_field_name='name',
        filter_field_value=TEST_EVENT['name']
        )

    # asserting test_event state before update
    assert event_object is not None
    assert int(event_object['attendees']) == int(TEST_EVENT['attendees'])

    test_event = TEST_EVENT
    test_event['attendees'] = 2

    returned_value = command.event_update(event_id=event_object['id'], event_data=test_event)
    assert int(returned_value[0]['attendees']) == 2
    assert returned_value[-1]['operation'] == 'update'

@pytest.mark.django_db
def test_event_delete_should_delete():
    command = event.Command()
    event_object = get_object_from_any_field(
        view_url='event',
        filter_field_name='name',
        filter_field_value=TEST_EVENT['name']
        )

    # asserting event is in DB before deleting
    assert event_object is not None

    returned_value = command.event_delete(event_id=event_object['id'])
    assert returned_value[0]['operation'] == 'delete'
