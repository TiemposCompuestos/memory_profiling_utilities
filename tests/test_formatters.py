import pytest

import memory_profiling_utilities.formatters as formatters
import memory_profiling_utilities.profilers as profilers

import testable_items


### FIXTURES

@pytest.fixture
def profile_output():
    profiler = profilers.make_class_profiler(testable_items.ExampleClass)
    @profiler
    def make_profile():
        instance = testable_items.ExampleClass()
        instance.first_method()
        instance.second_method()
    make_profile()
    output_line = ' '.join(formatters.generate_profile_table(make_profile))
    return output_line


### TESTS

def test_given_profile_when_format_profile_runs_return_formatted_profile():
    profile = '\n'.join([
        'Filename: /home/fede/Proyectos/memory_profiling_utilities/memory_profiling_utilities/profilers.py',
        '',
        'Line #    Mem usage    Increment   Line Contents',
        '================================================',
        '    29  18.8672 MiB  18.8672 MiB       def __init__(self):',
        '    30  18.8672 MiB   0.0000 MiB           pass',
        '',
        '',
        'Filename: /home/fede/Proyectos/memory_profiling_utilities/memory_profiling_utilities/profilers.py',
        '',
        'Line #    Mem usage    Increment   Line Contents',
        '================================================',
        '    31  18.8672 MiB  18.8672 MiB       def first_method(self):',
        "    32  18.8672 MiB   0.0000 MiB           return 'method number 1'",
        '',
        '',
        'Filename: /home/fede/Proyectos/memory_profiling_utilities/memory_profiling_utilities/profilers.py',
        '',
        'Line #    Mem usage    Increment   Line Contents',
        '================================================',
        '    33  18.8516 MiB  18.8516 MiB       def second_method(self):',
        "    34  18.8516 MiB   0.0000 MiB           return 'two'"
    ])
    formatted_profile = formatters.format_profile(profile)
    expected_formatted_profile = [
        'Filename\tLine #\tMem usage\tIncrement\tLine contents',
        '/home/fede/Proyectos/memory_profiling_utilities/memory_profiling_utilities/profilers.py\t29\t18.8672 MiB\t18.8672 MiB\tdef __init__(self):',
        '/home/fede/Proyectos/memory_profiling_utilities/memory_profiling_utilities/profilers.py\t30\t18.8672 MiB\t0.0000 MiB\t    pass',
        '/home/fede/Proyectos/memory_profiling_utilities/memory_profiling_utilities/profilers.py\t31\t18.8672 MiB\t18.8672 MiB\tdef first_method(self):',
        "/home/fede/Proyectos/memory_profiling_utilities/memory_profiling_utilities/profilers.py\t32\t18.8672 MiB\t0.0000 MiB\t    return 'method number 1'",
        '/home/fede/Proyectos/memory_profiling_utilities/memory_profiling_utilities/profilers.py\t33\t18.8516 MiB\t18.8516 MiB\tdef second_method(self):',
        "/home/fede/Proyectos/memory_profiling_utilities/memory_profiling_utilities/profilers.py\t34\t18.8516 MiB\t0.0000 MiB\t    return 'two'"
    ]
    assert formatted_profile == expected_formatted_profile

def test_given_profiling_sequence_when_profile_generated_return_table_with_correct_headers(profile_output):
    assert 'Filename\tLine #\tMem usage\tIncrement\tLine contents' in profile_output

def test_given_profiling_sequence_when_profile_generated_return_table_with_memory_usage_entries(profile_output):
    assert 'MiB' in profile_output

def test_given_profiling_sequence_when_profile_generated_return_table_with_constructor_profile(profile_output):
    assert '__init__' in profile_output

def test_given_profiling_sequence_when_profile_generated_return_table_with_first_method_profile(profile_output):
    assert 'first_method' in profile_output

def test_given_profiling_sequence_when_profile_generated_return_table_with_second_method_profile(profile_output):
    assert 'second_method' in profile_output
