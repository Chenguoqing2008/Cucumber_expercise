#! /usr/bin/python3
# _*_ coding:utf-8 _*_

from pathlib import Path
import os
import pytest
import pandas as pd

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


class ScheduleData:
    dataframe = pd.DataFrame(columns=['dummy'])

    def __init__(self, dataframe):
        self.__class__.dataframe = dataframe


@pytest.fixture
def pytestbdd_feature_base_dir():
    parent_path = Path(os.path.abspath(os.path.pardir))
    return os.path.join(os.path.abspath(parent_path.parent), 'features')


@scenario('Section1Rules.feature', 'schedule start and end date should match questionnaire')
def test_schedule_date():
    pass


@given("Schedule is generated and schedule data is trans-formatted to pandas")
def generate_schedule_data(schedule_object):
    ScheduleData(schedule_object)


@given("I am a store manager and i check the schedule")
def step_imp2():
    pass


@when("The schedule is generated")
def step_imp_tekd():
    pass


@then("All the store schedule begin and end date shall be 'Sun' and 'Sat'")
def step_imp3():
    assert ScheduleData.dataframe.head(0) == 'hello'
