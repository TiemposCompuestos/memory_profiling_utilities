import pytest

import memory_profiling_utilities.patchers as patchers

import testable_items

### FIXTURES

@pytest.fixture
def patch_list():
    return [
        ('testable_items.function_to_replace', lambda x: x),
        ('testable_items.variable_to_replace', 'replaced')
    ]

@pytest.fixture
def empty_patch_function():
    patch_function = patchers.make_batch_patcher([])
    @patch_function
    def patchable_function():
        return (
            testable_items.function_to_replace('palabra'),
            testable_items.variable_to_replace
        )
    return patchable_function

@pytest.fixture
def single_patch_function():
    def apply_patch(patch):
        patch_function = patchers.make_batch_patcher(patch)
        @patch_function
        def patchable_function():
            return (
                testable_items.function_to_replace('palabra'),
                testable_items.variable_to_replace
            )
        return patchable_function()
    return apply_patch

@pytest.fixture
def batch_patch_function(patch_list):
    patcher = patchers.make_batch_patcher(patch_list)
    @patcher
    def patchable_function():
        return (
            testable_items.function_to_replace('palabra'),
            testable_items.variable_to_replace
        )
    return patchable_function


### TESTS

def test_given_nothing_when_make_batch_patcher_decorates_patchable_then_leave_funtion_unpatched(
    empty_patch_function
):
    function_to_replace, _ = empty_patch_function()
    assert function_to_replace == 'function to replace prints: palabra'

def test_given_nothing_when_make_batch_patcher_decorates_patchable_then_leave_variable_unpatched(
    empty_patch_function
):
    _, variable_to_replace = empty_patch_function()
    assert variable_to_replace == 'variable to replace'

@pytest.mark.parametrize('patch, function_output', [
    ([('testable_items.function_to_replace', lambda x: x)], ('palabra')),
    ([('testable_items.variable_to_replace', 'replaced')], ('function to replace prints: palabra'))
])
def test_given_single_patch_when_make_batch_patcher_decorates_patchable_then_return_correct_function_output(
    patch,
    function_output,
    single_patch_function
):
    patched_function, _ = single_patch_function(patch)
    assert patched_function == function_output

@pytest.mark.parametrize('patch, variable_value', [
    ([('testable_items.function_to_replace', lambda x: x)], ('variable to replace')),
    ([('testable_items.variable_to_replace', 'replaced')], ('replaced'))
])
def test_given_single_patch_when_make_batch_patcher_decorates_patchable_then_return_correct_variable_value(
    patch,
    variable_value,
    single_patch_function
):
    _, patched_variable = single_patch_function(patch)
    assert patched_variable == variable_value

def test_given_patch_list_when_make_batch_patcher_decorates_patchable_then_return_correct_function_output(
    batch_patch_function
):
    
    patched_function, _ = batch_patch_function()
    assert patched_function == 'palabra'

def test_given_patch_list_when_make_batch_patcher_decorates_patchable_then_return_correct_variable_value(
    batch_patch_function
):
    _, patched_variable = batch_patch_function()
    assert patched_variable == 'replaced'