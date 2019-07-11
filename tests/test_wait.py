from unittest.mock import MagicMock, patch

from pypcom import PC

import pytest


class FakeComponentNoCustomExpectedConditions(PC):
    driver = None
    _parent = None
    _locator = ("id", "no-expected")


custom_callable_mock = MagicMock(return_value=True)


custom_condition_mock = MagicMock(return_value=custom_callable_mock)


def custom_query_condition(component, **query_details):
    def callable(driver):
        return component.query(**query_details)
    return callable


class FakeComponentHasCustomExpectedConditions(PC):
    driver = None
    _parent = None
    _expected_conditions = {
        "custom_condition": custom_condition_mock,
        "custom_query": custom_query_condition,
    }
    _locator = ("id", "expected")

    def query(self, **kwargs):
        return kwargs



class TestCustomCondition():

    @pytest.fixture(scope="class", autouse=True)
    def component(self):
        return FakeComponentHasCustomExpectedConditions()

    @pytest.fixture(scope="class", autouse=True)
    def wait(self, component):
        component.wait_until("custom_condition")

    def test_custom_condition_called_once(self):
        assert custom_condition_mock.call_count == 1

    def test_custom_callable_called_once(self):
        assert custom_condition_mock.call_count == 1


class TestVisibleCondition():

    @pytest.fixture(scope="class", autouse=True)
    def component(self):
        return FakeComponentHasCustomExpectedConditions()

    @pytest.fixture(scope="class", autouse=True)
    def mock_expected_visible_callable(self):
        return MagicMock(return_value=True)

    @pytest.fixture(scope="class", autouse=True)
    def mock_expected_visible_condition(self, mock_expected_visible_callable):
        from pypcom.component import expected_conditions
        with patch(
            "pypcom.component.expected_conditions.visible",
            return_value=mock_expected_visible_callable,
        ) as mock:
            yield mock

    @pytest.fixture(scope="class", autouse=True)
    def wait(self, component, mock_expected_visible_condition):
        component.wait_until("visible")

    def test_condition_called_once(self, mock_expected_visible_condition):
        assert mock_expected_visible_condition.call_count == 1

    def test_callable_called_once(self, mock_expected_visible_callable):
        assert mock_expected_visible_callable.call_count == 1


class TestCustomConditionNoCustoms():

    @pytest.fixture(scope="class", autouse=True)
    def component(self):
        return FakeComponentNoCustomExpectedConditions()

    @pytest.fixture(scope="class", autouse=True)
    def excinfo(self, component):
        with pytest.raises(KeyError) as excinfo:
            component.wait_until("custom_condition")
        return excinfo

    @pytest.fixture(scope="class", autouse=True)
    def exception_message(self, excinfo):
        return str(excinfo.value).strip("\"")

    def test_exception_raised(self, exception_message):
        assert exception_message == "Condition 'custom_condition' is not supported"


class TestVisibleConditionNoCustoms():

    @pytest.fixture(scope="class", autouse=True)
    def component(self):
        return FakeComponentNoCustomExpectedConditions()

    @pytest.fixture(scope="class", autouse=True)
    def mock_expected_visible_callable(self):
        return MagicMock(return_value=True)

    @pytest.fixture(scope="class", autouse=True)
    def mock_expected_visible_condition(self, mock_expected_visible_callable):
        from pypcom.component import expected_conditions
        with patch(
            "pypcom.component.expected_conditions.visible",
            return_value=mock_expected_visible_callable,
        ) as mock:
            yield mock

    @pytest.fixture(scope="class", autouse=True)
    def wait(self, component, mock_expected_visible_condition):
        component.wait_until("visible")

    def test_condition_called_once(self, mock_expected_visible_condition):
        assert mock_expected_visible_condition.call_count == 1

    def test_callable_called_once(self, mock_expected_visible_callable):
        assert mock_expected_visible_callable.call_count == 1


class TestDirectCallableCondition():

    @pytest.fixture(scope="class", autouse=True)
    def component(self):
        return FakeComponentHasCustomExpectedConditions()

    @pytest.fixture(scope="class", autouse=True)
    def mock_direct_callable(self):
        return MagicMock(return_value=True)

    @pytest.fixture(scope="class", autouse=True)
    def mock_direct_condition(self, mock_direct_callable):
        return MagicMock(return_value=mock_direct_callable)

    @pytest.fixture(scope="class", autouse=True)
    def wait(self, component, mock_direct_condition):
        component.wait_until(mock_direct_condition)

    def test_condition_called_once(self, mock_direct_condition):
        assert mock_direct_condition.call_count == 1

    def test_callable_called_once(self, mock_direct_callable):
        assert mock_direct_callable.call_count == 1


class TestCustomConditionWithExtraKwargs():

    @pytest.fixture(scope="class", autouse=True)
    def component(self):
        return FakeComponentHasCustomExpectedConditions()

    @pytest.fixture(scope="class", autouse=True)
    def query_details(self):
        return {"a": "apple"}

    @pytest.fixture(scope="class", autouse=True)
    def wait(self, component, query_details):
        return component.wait_until("custom_query", **query_details)

    @pytest.fixture(scope="class", autouse=True)
    def wait_result(self, wait):
        return wait

    def test_additional_kwargs_were_passed_down(self, wait_result, query_details):
        assert wait_result == query_details
