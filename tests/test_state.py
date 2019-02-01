import pytest

from pypcom import State
from pypcom.state import (
    IsPresent,
    IsDisplayed,
    IsEnabled,
)


class FakeComponent(object):
    def __init__(self, is_present=True, is_displayed=True, is_enabled=True):
        self._is_present = is_present
        self._is_displayed = is_displayed
        self._is_enabled = is_enabled

    def is_present(self):
        return self._is_present

    def is_displayed(self):
        return self._is_displayed

    def is_enabled(self):
        return self._is_enabled


@pytest.fixture(scope="class")
def fake_component():
    return FakeComponent(is_present=False, is_displayed=False, is_enabled=True)

@pytest.fixture(scope="class")
def state():
    return State(
        IsPresent(True),
        IsDisplayed(True),
        IsEnabled(True),
    )

@pytest.fixture(scope="class")
def expected_pytest_report_repr(fake_component):
    return [
        "Comparing {} State:".format(fake_component.__class__.__name__),
        "    {}: {}".format(
            IsPresent().get_name(),
            IsPresent._msg[True],
        ),
        "    {}: {}".format(
            IsDisplayed().get_name(),
            IsDisplayed._msg[True],
        ),
    ]

@pytest.fixture(scope="class", autouse=True)
def comparison_result(fake_component, state):
    return fake_component == state


@pytest.fixture(scope="class", autouse=True)
def pytest_report_repr(comparison_result, state):
    return state.get_pytest_failure_report_repr()


class TestState(object):

    def test_comparison_result(self, comparison_result):
        assert comparison_result is False

    def test_pytest_report_repr(self, pytest_report_repr,
                                expected_pytest_report_repr):
        assert pytest_report_repr == expected_pytest_report_repr