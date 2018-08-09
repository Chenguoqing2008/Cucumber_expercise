#! /usr/bin/python3
# _*_ coding:utf-8 _*_

from pathlib import Path
import os
import pytest

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)

schedule_object = None


@pytest.fixture
def pytestbdd_feature_base_dir():
    parent_path = Path(os.path.abspath(os.path.pardir))
    return os.path.join(os.path.abspath(parent_path.parent), 'features')


@given("I have injecting given", target_fixture="foo")
def injecting_given():
    return "injected foo"


@then('foo should be "injected foo"')
def foo_is_foo(foo):
    assert foo == 'injected foo'


@scenario("Section1Rules.feature", 'Test given fixture injection')
def test_test_given_fixture_injection():
    pass


# @given("Schedule is generated and schedule data is trans-formatted to pandas")
# def step_impl(schedule_object):
#     schedule_object = schedule_object
#

# @given("I am a store manager and i check the schedule")
# def step_impl():
#     pass
#
#
# @when("The schedule is generated")
# def step_impl():
#     pass
#
#
# @then("All the store schedule begin and end date shall be 'Sun' and 'Sat'")
# def step_impl():
#     pass
