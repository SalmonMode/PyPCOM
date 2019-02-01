from pypcom import State


def pytest_assertrepr_compare(config, op, left, right):
    state = None
    if op == "==":
        if isinstance(left, State):
            state = left
        elif isinstance(right, State):
            state = right
        else:
            return
        return state.get_pytest_failure_report_repr()