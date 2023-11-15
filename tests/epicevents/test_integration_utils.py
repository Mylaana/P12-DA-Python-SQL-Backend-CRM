from Client.management.commands import client
import pytest
from unittest.mock import patch
from EpicEvents.utils import get_ee_contact_id, request_commands
from UserProfile.models import UserProfile

@pytest.mark.django_db
def test_geteecontactid_should_return_none():
    result = get_ee_contact_id('not_existing_contact')

    assert result is None
"""
@pytest.mark.django_db
def test_geteecontactid_should_return_id():
    ee_contact_name = 'user1'
    result = get_ee_contact_id(ee_contact_name)
    print(result)
    assert result is not None
"""

"""
@pytest.mark.django_db
def test_requestcommand_should_create_client():
    client_data = {
        'name': 'test_client',
        'siren': 'siren000',
        'email': 'email@client.com',
        'phone': '0000',
        'client_contact_name': 'contact',
        'information': 'info000',
        'date_creation': '2023-10-30T10:52:06.993607Z',
        'date_update': '2023-10-31T09:30:42.559786Z',
        'ee_contact': 0,
        'ee_contact_name': 'ee_contact_name',
        'ee_contact_id': 0
    }
    client_data = {
        'ee_contact': ee_contact_id,
        'name': "",
        'siren': "",
        'client_contact_name': "",
        'email': "",
        'phone': "",
        'information':""
    }
    result = request_commands(
        view_url='client',
        operation='create',
        request_data=client_data
        )
    expected_result = 'test_client'

    assert expected_result in result

@pytest.mark.django_db
def test_requestcommand_should_return_list():
    result = request_commands(
        view_url='client',
        operation='read',
        )
    expected_result = 'test_client'

    assert expected_result in result
"""