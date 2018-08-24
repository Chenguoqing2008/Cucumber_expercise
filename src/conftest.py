
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
    print("##########start_date##################" + start_date)
    end_date = request.config.getoption('end')[0]
    print("##########end_date##################" + end_date)
    scheduleobject = ScheduleObject(start_date, end_date)
    # test_data = scheduleobject.schedule_dataframe.shape(1)
    print(type(scheduleobject))
    # print(scheduleobject.schedule_dataframe.head(2))
    return scheduleobject.schedule_dataframe

