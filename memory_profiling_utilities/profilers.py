import inspect

from memory_profiler import profile

from memory_profiling_utilities.patchers import make_batch_patcher


def make_class_profiler(class_to_profile, overriding_patches = dict()):
    class_name = '.'.join([class_to_profile.__module__, class_to_profile.__name__])
    class_methods = inspect.getmembers(class_to_profile, inspect.isfunction)
    class_patches = [
        (
            '.'.join([class_name, method_name]),
            profile(method, precision = 4)
        ) for method_name, method in class_methods if not
        method_name in overriding_patches.keys()
    ]
    overridden_patches = [
        (
            '.'.join([class_name, method_name]),
            profile(overriding_patches[method_name], precision = 4)
        ) for method_name in overriding_patches.keys() if
        inspect.isfunction(overriding_patches[method_name])
    ]
    class_profiler = make_batch_patcher(class_patches + overridden_patches)
    return class_profiler

class ExampleClass:
    def __init__(self):
        pass
    def first_method(self):
        return 'method number 1'
    def second_method(self):
        return 'two'