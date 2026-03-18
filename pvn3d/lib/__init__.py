from __future__ import (
    division,
    absolute_import,
    with_statement,
    print_function,
    unicode_literals,
)
import importlib

__all__ = ["PVN3D"]


def __getattr__(name):
    if name == "PVN3D":
        return importlib.import_module(".pvn3d", __name__).PVN3D

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
