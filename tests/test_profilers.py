import pytest

import memory_profiling_utilities.profilers as profilers

import testable_items


### FIXTURES

@pytest.fixture
def complete_class_profiling():
    profiler = profilers.make_class_profiler(testable_items.ExampleClass)
    @profiler
    def profile_class():
        instance = testable_items.ExampleClass()
        instance.first_method()
        instance.second_method()
    profile_class()

@pytest.fixture
def empty_overridden_class_profiling():
    profiler = profilers.make_class_profiler(
        testable_items.ExampleClass,
        overriding_patches = {'second_method': None}
    )
    @profiler
    def profile_class():
        instance = testable_items.ExampleClass()
        instance.first_method()
        instance.second_method()
    profile_class()

@pytest.fixture
def overridden_method_class_profiling():
    def overriding_method(self):
        return 'overridden method'
    profiler = profilers.make_class_profiler(
        testable_items.ExampleClass,
        overriding_patches = {'second_method': overriding_method}
    )
    @profiler
    def profile_class():
        instance = testable_items.ExampleClass()
        instance.first_method()
        instance.second_method()
    profile_class()


### TESTS

def test_given_testable_class_when_make_class_profler_runs_profile_constructor(
    capsys,
    complete_class_profiling
):
    profile = str(capsys.readouterr())
    assert 'def __init__' in profile

def test_given_testable_class_when_make_class_profler_runs_profile_first_method(
    capsys,
    complete_class_profiling
):
    profile = str(capsys.readouterr())
    assert 'def first_method' in profile

def test_given_testable_class_when_make_class_profler_runs_profile_second_method(
    capsys,
    complete_class_profiling
):
    profile = str(capsys.readouterr())
    assert 'def second_method' in profile

def test_given_testable_class_and_empty_overriding_method_when_make_class_profler_runs_profile_constructor(
    capsys,
    empty_overridden_class_profiling
):
    profile = str(capsys.readouterr())
    assert 'def __init__' in profile

def test_given_testable_class_and_empty_overriding_method_when_make_class_profler_runs_profile_first_method(
    capsys,
    empty_overridden_class_profiling
):
    profile = str(capsys.readouterr())
    assert 'def first_method' in profile

def test_given_testable_class_and_empty_overriding_method_when_make_class_profler_runs_dont_profile_second_method(
    capsys,
    empty_overridden_class_profiling
):
    profile = str(capsys.readouterr())
    assert 'def second_method' not in profile

def test_given_testable_class_and_alternative_overriding_method_when_make_class_profler_runs_profile_overridden_method(
    capsys,
    overridden_method_class_profiling
):
    
    profile = str(capsys.readouterr())
    assert 'def overriding_method' in profile