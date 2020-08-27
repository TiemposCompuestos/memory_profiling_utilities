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


### TESTS

def test_given_nothing_when_make_batch_patcher_decorates_patchable_then_patch_nothing():
    patch_function = patchers.make_batch_patcher([])
    @patch_function
    def patchable_function():
        return (
            testable_items.function_to_replace('palabra'),
            testable_items.variable_to_replace
        )
    function_to_replace, variable_to_replace = patchable_function()
    condition_1 = function_to_replace == 'function to replace prints: palabra'
    condition_2 = variable_to_replace == 'variable to replace'
    assert condition_1 and condition_2

@pytest.mark.parametrize('patch, expected_output', [
    (
        [('testable_items.function_to_replace', lambda x: x)],
        ('palabra', 'variable to replace')
    ),
    (
        [('testable_items.variable_to_replace', 'replaced')],
        ('function to replace prints: palabra', 'replaced')
    )
])
def test_given_single_patch_when_make_batch_patcher_decorates_patchable_then_return_expected_output(
    patch,
    expected_output
):
    patcher = patchers.make_batch_patcher(patch)
    @patcher
    def patchable_function():
        return (
            testable_items.function_to_replace('palabra'),
            testable_items.variable_to_replace
        )
    patched_function, patched_variable = patchable_function()
    condition_1 = patched_function == expected_output[0]
    condition_2 = patched_variable == expected_output[1]
    assert condition_1 and condition_2

def test_given_patch_list_when_make_batch_patcher_decorates_patchable_then_return_expected_output(
    patch_list
):
    patcher = patchers.make_batch_patcher(patch_list)
    @patcher
    def patchable_function():
        return (
            testable_items.function_to_replace('palabra'),
            testable_items.variable_to_replace
        )
    patched_function, patched_variable = patchable_function()
    condition_1 = patched_function == 'palabra'
    condition_2 = patched_variable == 'replaced'
    assert condition_1 and condition_2