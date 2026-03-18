from __future__ import (
    division,
    absolute_import,
    with_statement,
    print_function,
    unicode_literals,
)
import importlib

__all__ = ["pointnet2_utils", "pointnet2_modules", "_ext"]


def __getattr__(name):
    if name in __all__:
        return importlib.import_module(f"{__name__}.{name}")

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
