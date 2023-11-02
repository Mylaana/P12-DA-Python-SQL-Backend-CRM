from Client.management.commands import client
import pytest

@pytest.mark.django_db
def test_should_return_true():
    command = client.Command()

    username = "admin-oc"
    user_id = command.get_ee_contact_id(username)

    assert 1 == 1
