from UserProfile.models import UserProfile, Team
from UserProfile.management.commands import user
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input
import time
from EpicEvents.utils import get_object_field_from_id, get_object_from_any_field
import json


TEST_USER = {'username': 'test_user',
             'password': 'test_password123$A',
             'team': '1',
             'email': 'test_user@ee.com',
             'first_name': 'test user prenom',
             'last_name': 'test user nom',
             'phone': '0000000000'}

@pytest.mark.django_db
def test_user_create_should_create():
    command = user.Command()
    returned_value = command.user_create(TEST_USER)
    assert returned_value[0]['username'] == TEST_USER['username']

@pytest.mark.django_db
def test_user_list_should_list():
    command = user.Command()
    returned_value = command.user_list()
    assert TEST_USER['username'] in returned_value

@pytest.mark.django_db
def test_user_read_should_return_user_info():
    command = user.Command()
    user_object = get_object_from_any_field(
        view_url='user',
        filter_field_name='username',
        filter_field_value=TEST_USER['username']
        )

    returned_value = command.user_read(user_id=user_object['id'])

    assert user_object is not None
    assert user_object['username'] == TEST_USER['username']

@pytest.mark.django_db
def test_user_update_should_update():
    command = user.Command()
    user_object = get_object_from_any_field(
        view_url='user',
        filter_field_name='username',
        filter_field_value=TEST_USER['username']
        )

    # asserting test_user state before update
    assert user_object is not None
    assert user_object['phone'] == TEST_USER['phone']

    test_user = TEST_USER
    test_user['phone'] = 111

    returned_value = command.user_update(user_id=user_object['id'], user_data=test_user)
    assert str(returned_value[0]['phone']) == '111'
    assert returned_value[-1]['operation'] == 'update'

@pytest.mark.django_db
def test_user_delete_should_delete():
    command = user.Command()
    user_object = get_object_from_any_field(
        view_url='user',
        filter_field_name='username',
        filter_field_value=TEST_USER['username']
        )

    # asserting user is in DB before deleting
    assert user_object is not None

    returned_value = command.user_delete(user_id=user_object['id'])
    assert returned_value[0]['operation'] == 'delete'
