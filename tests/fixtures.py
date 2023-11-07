import pytest

@pytest.fixture
def simulate_user_input(monkeypatch):
    user_inputs = []

    def input_mock(prompt):
        if user_inputs:
            return user_inputs.pop(0)
        raise ValueError("Not enough user inputs provided")

    def _simulate_user_input(inputs):
        nonlocal user_inputs
        user_inputs = inputs

    monkeypatch.setattr('builtins.input', input_mock)
    return _simulate_user_input