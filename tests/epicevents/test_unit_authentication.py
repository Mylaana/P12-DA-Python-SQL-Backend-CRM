import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input
from EpicEvents import authentication
from tests.conftest import SETUP_USER_FIELDS

@patch('EpicEvents.authentication.getpass', Mock(return_value='invalid_password'))
def test_request_token_should_404(simulate_user_input, capfd):
    simulate_user_input(['invalid_id'])
    result = authentication.request_get_token()

    out, err = capfd.readouterr()
    assert 'response status code: 400' in out

@patch('EpicEvents.authentication.getpass', Mock(return_value=SETUP_USER_FIELDS['password']))
def test_request_token_should_succeed(simulate_user_input, capfd):
    simulate_user_input([SETUP_USER_FIELDS['username']])
    result = authentication.request_get_token()
    print(result)
    out, err = capfd.readouterr()
    assert SETUP_USER_FIELDS['username'] in out
    assert 'token' in out
