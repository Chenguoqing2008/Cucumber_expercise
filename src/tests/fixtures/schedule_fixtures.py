import pytest
from util.ScheduleObject import ScheduleObject
import sys


@pytest.fixture
def foo():
    return "foo"


@pytest.fixture
def schedule_dataframe():
    schedule_object = ScheduleObject(sys.argv[1], sys.argv[2])
    return schedule_object.shedule_dataframe


