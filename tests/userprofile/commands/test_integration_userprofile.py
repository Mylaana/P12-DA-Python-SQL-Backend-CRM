from UserProfile.models import UserProfile, Team
from UserProfile.management.commands import user
import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input
import time
from EpicEvents.utils import get_ee_contact_id
import json

TEST_USER = {'username': 'test_user',
             'password': 'test_password123$A',
             'team': '1',
             'email': 'test_user@ee.com',
             'first_name': 'test user prenom',
             'last_name': 'test user nom',
             'phone': '0000000000'}
"""
@pytest.mark.django_db
@patch('UserProfile.management.commands.user.getpass', Mock(return_value='test_password123$A'))
def test_handle_create_should_create_user(capfd, simulate_user_input):
    simulate_user_input(
        [TEST_USER['username'],
        TEST_USER['password'],
        TEST_USER['team'],
        TEST_USER['email'],
        TEST_USER['first_name'],
        TEST_USER['last_name'],
        TEST_USER['phone']
        ])

    call_command('user', '-create')
    out, err = capfd.readouterr()
    expected_value = f"Utilisateur '{TEST_USER['username']}' créé avec succès"
    expected_user_data = {}
    user = UserProfile.objects.filter(username=TEST_USER['username']).first()
    print(user)
    assert user is not None
    # assert expected_value.strip().lower() in out.strip().lower()
"""


@pytest.mark.django_db
def test_handle_create_user_should_create():
    command = user.Command()
    returned_value = command.user_create(TEST_USER)
    # parsed_value = json.loads(returned_value)

    assert TEST_USER['username'] in returned_value
    user_id = get_ee_contact_id(username=TEST_USER['username'])
    print(user_id)
    assert user_id is not None

@pytest.mark.django_db
def test_handle_delete_user_should_delete():
    command = user.Command()
    time.sleep(1)
    user_id = get_ee_contact_id(username=TEST_USER['username'])
    print(TEST_USER['username'])
    print(user_id)
    user_id = get_ee_contact_id(username=TEST_USER['username'])
    assert user_id is not None
    returned_value = command.user_delete(user_id=user_id)

    # assert returned_value == 'delete'
    user_id = get_ee_contact_id(username=TEST_USER['username'])
    assert user_id is None
