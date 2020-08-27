import pytest

import memory_profiling_utilities.formatters as formatters
import memory_profiling_utilities.profilers as profilers

import testable_items


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
    print(*formatted_profile, sep = '\n')
    print(*expected_formatted_profile, sep = '\n')
    assert formatted_profile == expected_formatted_profile

def test_given_profiling_sequence_when_profile_generated_return_table():
    profiler = profilers.make_class_profiler(profilers.ExampleClass)
    @profiler
    def make_profile():
        instance = profilers.ExampleClass()
        instance.first_method()
        instance.second_method()
    output_line = ' '.join(formatters.generate_profile_table(make_profile))
    print(output_line)
    condition_1 = 'Filename\tLine #\tMem usage\tIncrement\tLine contents' in output_line
    condition_2 = 'MiB' in output_line
    condition_3 = '__init__' in output_line
    condition_4 = 'first_method' in output_line
    condition_5 = 'second_method' in output_line
    assert condition_1 and condition_2 and condition_3 and condition_4 and condition_5

