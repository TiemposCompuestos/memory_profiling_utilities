import re
import sys
from io import StringIO

import memory_profiling_utilities.profilers as profilers


def format_profile(profile):
    headers = ['Filename', 'Line #', 'Mem usage', 'Increment', 'Line contents']
    out_lines = ['{}\t{}\t{}\t{}\t{}'.format(*headers)]
    filename = ''
    for line in profile.split('\n'):
        if 'Filename' in line:
            filename = re.sub('Filename: ', '', line)
        if 'MiB' in line:
            data, code = line.split('       ')
            _, line_n, mem_usage, mem_increment = re.sub('   +', '  ', data).split('  ')
            record = '{}\t{}\t{}\t{}\t{}'.format(
                filename,
                line_n,
                mem_usage,
                mem_increment,
                code
            )
            out_lines.append(record)
    return out_lines

def generate_profile_table(profiling_function):
    buffer = StringIO()
    sys.stdout = buffer
    profiling_function()
    sys.stdout = sys.__stdout__
    profile = buffer.getvalue()
    return format_profile(profile)



profiler = profilers.make_class_profiler(profilers.ExampleClass)
@profiler
def make_profile():
    instance = profilers.ExampleClass()
    instance.first_method()
    instance.second_method()


out = generate_profile_table(make_profile)
print(out)