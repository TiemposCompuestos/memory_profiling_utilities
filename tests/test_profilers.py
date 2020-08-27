import pytest

import memory_profiling_utilities.profilers as profilers

import testable_items


def test_given_testable_class_when_make_class_profler_runs_profile_all_methods(
    capsys
):
    profiler = profilers.make_class_profiler(testable_items.ExampleClass)
    @profiler
    def profile_class():
        instance = testable_items.ExampleClass()
        instance.first_method()
        instance.second_method()
    profile_class()
    profile = str(capsys.readouterr())
    condition_1 = 'def __init__' in profile
    condition_2 = 'def first_method' in profile
    condition_3 = 'def second_method' in profile
    assert condition_1 and condition_2 and condition_3

def test_given_testable_class_and_empty_overriding_method_when_make_class_profler_runs_profile_all_methods(
    capsys
):
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
    profile = str(capsys.readouterr())
    condition_1 = 'def __init__' in profile
    condition_2 = 'def first_method' in profile
    condition_3 = 'def second_method' not in profile
    assert condition_1 and condition_2 and condition_3

def test_given_testable_class_and_alternative_overriding_method_when_make_class_profler_runs_profile_all_methods(
    capsys
):
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
    profile = str(capsys.readouterr())
    condition_1 = 'def __init__' in profile
    condition_2 = 'def first_method' in profile
    condition_3 = 'def second_method' not in profile
    condition_4 = 'def overriding_method' in profile
    assert condition_1 and condition_2 and condition_3 and condition_4