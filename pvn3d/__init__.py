from __future__ import (
    division,
    absolute_import,
    with_statement,
    print_function,
    unicode_literals,
)
import importlib

__version__ = "2.1.1"

try:
    __PVN3D_SETUP__
except NameError:
    __PVN3D_SETUP__ = False

__all__ = ["pointnet2_utils"]


def __getattr__(name):
    if __PVN3D_SETUP__:
        raise AttributeError(name)

    if name == "pointnet2_utils":
        return importlib.import_module("pvn3d.lib.pointnet2_utils")

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
