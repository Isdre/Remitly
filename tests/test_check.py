import sys
import os

project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

import pytest
from JsonChecker import *


def test_check_0():
    with pytest.raises(TypeError):
        obj = JsonChecker("tests\\test_0.txt")

    assert type_check(str,"string") is True
    assert type_check(dict, {}) is True
    assert type_check(str, {}) is False
    assert type_check(int, "0") is False

def test_check_1():
    obj = JsonChecker("tests\\test_1.json")
    assert obj.check()

def test_check_2():
    obj = JsonChecker("tests\\test_2.json")
    assert obj.check()

def test_check_3():
    obj = JsonChecker("tests\\test_3.json")
    assert obj.check()

def test_check_4():
    obj = JsonChecker("tests\\test_4.json")
    assert obj.check()

def test_check_5():
    obj = JsonChecker("tests\\test_5.json")
    assert obj.check() == False