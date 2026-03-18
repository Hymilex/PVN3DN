#!/usr/bin/env python3
import glob
import shutil
from pathlib import Path
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension


_ext_src_root = "./pvn3d/_ext-src"
_ext_sources = glob.glob("{}/src/*.cpp".format(_ext_src_root)) + glob.glob(
    "{}/src/*.cu".format(_ext_src_root)
)
_ext_headers = glob.glob("{}/include/*".format(_ext_src_root))
_package_ext_dir = Path("pvn3d/lib/pointnet2_utils")


class BuildExtAndCopy(BuildExtension):
    # The default inplace copy logic uses the extension name to derive a source
    # package path. This project builds the extension under build/ first and then
    # copies the resulting .so into pvn3d/lib/pointnet2_utils manually below.
    def copy_extensions_to_source(self):
        return

    def run(self):
        super().run()

        candidates = list(Path(self.build_lib).rglob("_ext*.so"))
        if not candidates:
            candidates = list(Path("build").rglob("_ext*.so"))
        if not candidates:
            raise FileNotFoundError("Cannot find built pointnet2 extension under build/")

        built_ext = max(candidates, key=lambda p: p.stat().st_mtime)
        target_ext = _package_ext_dir / built_ext.name
        _package_ext_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(built_ext, target_ext)
        print(f"{built_ext} ==> {target_ext}")


setup(
    name='pvn3d',
    ext_modules=[
        CUDAExtension(
            name='pvn3d.lib.pointnet2_utils._ext',
            sources=_ext_sources,
            extra_compile_args={
                "cxx": ["-O2", "-I{}".format("{}/include".format(_ext_src_root))],
                "nvcc": [
                    "-O2", "-I{}".format("{}/include".format(_ext_src_root))
                ],
            },
        )
    ],
    cmdclass={
        'build_ext': BuildExtAndCopy
    }
)

# vim: ts=4 sw=4 sts=4 expandtab
