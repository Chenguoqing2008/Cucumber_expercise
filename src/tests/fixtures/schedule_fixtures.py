import pytest
import logging

stepslog = logging.getLogger('schedule_dataframe')


@pytest.fixture
def foo():
    return "foo"


