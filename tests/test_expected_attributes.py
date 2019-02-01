import pytest

from pypcom import State
from pypcom.state import (
    IsPresent,
    IsDisplayed,
    IsEnabled,
    TagName,
    Href,
    Text,
    Placeholder,
    Type,
)


class FakeComponent(object):
    def __init__(self, is_present=True, is_displayed=True, is_enabled=True,
                 tag_name=None, href=None, text=None, placeholder=None,
                 type_=None):
        self._is_present = is_present
        self._is_displayed = is_displayed
        self._is_enabled = is_enabled
        self.tag_name = tag_name
        self._href = href
        self.text = text
        self._placeholder = placeholder
        self._type = type_

    def is_present(self):
        return self._is_present

    def is_displayed(self):
        return self._is_displayed

    def is_enabled(self):
        return self._is_enabled

    def get_attribute(self, attr):
        return getattr(self, "_{}".format(attr))


params = [
    (IsPresent(True), FakeComponent(is_present=True), []),
    (IsPresent(False), FakeComponent(is_present=False), []),
    (
        IsPresent(True),
        FakeComponent(is_present=False),
        [
            "    {}: {}".format(
                IsPresent().get_name(),
                IsPresent._msg[True],
            ),
        ],
    ),
    (
        IsPresent(False),
        FakeComponent(is_present=True),
        [
            "    {}: {}".format(
                IsPresent().get_name(),
                IsPresent._msg[False],
            ),
        ],
    ),
    (IsDisplayed(True), FakeComponent(is_displayed=True), []),
    (IsDisplayed(False), FakeComponent(is_displayed=False), []),
    (
        IsDisplayed(True),
        FakeComponent(is_displayed=False),
        [
            "    {}: {}".format(
                IsDisplayed().get_name(),
                IsDisplayed._msg[True],
            ),
        ],
    ),
    (
        IsDisplayed(False),
        FakeComponent(is_displayed=True),
        [
            "    {}: {}".format(
                IsDisplayed().get_name(),
                IsDisplayed._msg[False],
            ),
        ],
    ),
    (IsEnabled(True), FakeComponent(is_enabled=True), []),
    (IsEnabled(False), FakeComponent(is_enabled=False), []),
    (
        IsEnabled(True),
        FakeComponent(is_enabled=False),
        [
            "    {}: {}".format(
                IsEnabled().get_name(),
                IsEnabled._msg[True],
            ),
        ],
    ),
    (
        IsEnabled(False),
        FakeComponent(is_enabled=True),
        [
            "    {}: {}".format(
                IsEnabled().get_name(),
                IsEnabled._msg[False],
            ),
        ],
    ),
    (TagName("a"), FakeComponent(tag_name="a"), []),
    (TagName("p"), FakeComponent(tag_name="p"), []),
    (
        TagName("a"),
        FakeComponent(tag_name="p"),
        [
            "    {}: {}".format(
                TagName().get_name(),
                "'{}' is not '{}'".format("p", "a"),
            ),
        ],
    ),
    (Href("a"), FakeComponent(href="a"), []),
    (Href("p"), FakeComponent(href="p"), []),
    (
        Href("a"),
        FakeComponent(href="p"),
        [
            "    {}: {}".format(
                Href().get_name(),
                "'{}' is not '{}'".format("p", "a"),
            ),
        ],
    ),
    (Text("a"), FakeComponent(text="a"), []),
    (Text("p"), FakeComponent(text="p"), []),
    (
        Text("a"),
        FakeComponent(text="p"),
        [
            "    {}: {}".format(
                Text().get_name(),
                "'{}' is not '{}'".format("p", "a"),
            ),
        ],
    ),
    (Placeholder("a"), FakeComponent(placeholder="a"), []),
    (Placeholder("p"), FakeComponent(placeholder="p"), []),
    (
        Placeholder("a"),
        FakeComponent(placeholder="p"),
        [
            "    {}: {}".format(
                Placeholder().get_name(),
                "'{}' is not '{}'".format("p", "a"),
            ),
        ],
    ),
    (Type("a"), FakeComponent(type_="a"), []),
    (Type("p"), FakeComponent(type_="p"), []),
    (
        Type("a"),
        FakeComponent(type_="p"),
        [
            "    {}: {}".format(
                Type().get_name(),
                "'{}' is not '{}'".format("p", "a"),
            ),
        ],
    ),
]

@pytest.fixture(params=params)
def scenario_details(request):
    return request.param

@pytest.fixture
def expected_attribute(scenario_details):
    return scenario_details[0]

@pytest.fixture
def fake_component(scenario_details):
    return scenario_details[1]

@pytest.fixture
def expected_report_messages(scenario_details):
    return scenario_details[2]

@pytest.fixture(autouse=True)
def safe_compare(expected_attribute, fake_component):
    expected_attribute.safe_compare(fake_component)

@pytest.fixture
def actual_report_messages(safe_compare, expected_attribute):
    return expected_attribute.get_report_messages()

def test_expected_attribute(actual_report_messages, expected_report_messages):
    assert actual_report_messages == expected_report_messages
