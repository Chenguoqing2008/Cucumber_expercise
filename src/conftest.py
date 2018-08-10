#! /usr/bin/python3
# _*_ coding:utf-8 _*_

import pytest
from util.ScheduleObject import ScheduleObject


def pytest_addoption(parser):
    parser.addoption("--start",  action="append", default=[],
                     help="please input the start date of schedule")
    parser.addoption("--end", action="append", default=[],
                     help="please input the end date of schedule")


def pytest_generate_tests(metafunc):
    if 'fix' in metafunc.fixturenames:
        metafunc.parametrize("fix",
                             [metafunc.config.getoption('start'), metafunc.config.getoption('end')])


@pytest.fixture
def schedule_object(request):
    start_date = request.config.getoption('start')[0]
    end_date = request.config.getoption('end')[0]
    scheduleobject = ScheduleObject(start_date, end_date)
    return scheduleobject.shedule_dataframe

