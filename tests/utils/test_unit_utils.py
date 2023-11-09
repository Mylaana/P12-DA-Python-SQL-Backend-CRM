import pytest
from unittest.mock import patch, Mock
from django.core.management import call_command
from tests.fixtures import simulate_user_input
from EpicEvents import utils

def test_utils_input_validated_should_return_false():
    assert utils.input_validated("") == False

def test_utils_input_validated_should_return_true():
    assert utils.input_validated("somethin") == True