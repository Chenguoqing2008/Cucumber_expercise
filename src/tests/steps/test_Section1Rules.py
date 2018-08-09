#! /usr/bin/python3
# _*_ coding:utf-8 _*_
import pytest
import os
from pathlib import Path
# from util.ScheduleObject import ScheduleObject

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@pytest.fixture
def pytestbdd_feature_base_dir():
    parent_path = Path(os.path.abspath(os.path.pardir))
    return os.path.join(os.path.abspath(parent_path.parent), 'features')


@scenario("Section1Rules.feature", 'Test given fixture injection')
def test_test_given_fixture_injection():
    """Test given fixture injection."""


@given("I have injecting given", target_fixture="foo")
def injecting_given():
    return "injected foo"


@then('foo should be "injected foo"')
def foo_is_foo(foo):
    assert foo == 'injected foo'


@then("fixture test should win")
def step_impl(schedule_object):
    assert schedule_object == 'hello'

