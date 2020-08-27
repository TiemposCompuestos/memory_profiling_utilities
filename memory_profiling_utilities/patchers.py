from functools import reduce
from unittest.mock import patch

def make_batch_patcher(patches):
    batch_patch = reduce(
        lambda f, g: lambda x: g(f(x)),
        [patch(*args) for args in patches],
        lambda x: x
    )
    return batch_patch
