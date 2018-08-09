#! /usr/bin/python3
# _*_ coding:utf-8 _*_

from pathlib import Path
import os
import pytest

from pytest_bdd import (
    given,
    scenario,
    then,
)


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


@scenario('Section1Rules.feature', 'Test given fixture injection')
def test_given_fixture_injection():
    pass

