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
    # dataframe = pd.DataFrame(columns=['dummy'])
    #
    # def __init__(self, dataframe):
    #     self.__class__.dataframe = dataframe
    pass


@pytest.fixture
def pytestbdd_feature_base_dir():
    parent_path = Path(os.path.abspath(os.path.pardir))
    return os.path.join(os.path.abspath(parent_path.parent), 'features')


@scenario('Section1Rules.feature', 'schedule start and end date should match questionnaire')
def test_schedule_date():
    pass


@given("Schedule is generated and schedule data is trans-formatted to pandas")
def generate_schedule_data(schedule_object):
    ScheduleData.data = schedule_object


@given("I am a store manager and i want to check the schedule")
def store_manager_walkin():
    pass


@then("The store schedule date shall begin at <begin_weekday> and end at <end_weekday>")
def check_store_schedule_begin_end_weekdat(begin_weekday, end_weekday):
    storeid = ScheduleData.storelist[0]
    assert storeid == '862'
    # begin_date = ScheduleData.data.loc['storeid' == storeid]
    assert ScheduleData.data.head(0) == 'hello'


@when("I select the store id <storeid>")
def select_storeid(storeid):
    ScheduleData.storelist = []
    ScheduleData.storelist.append(storeid)

