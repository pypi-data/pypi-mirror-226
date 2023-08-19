from pathlib import Path

import numpy as np
from setuptools import Extension, find_packages, setup

project_dir = Path(__file__).parent.resolve()
long_description = (project_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="cougar",
    version="0.5.13",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yunchong Gan",
    author_email="yunchong@pku.edu.cn",
    packages=find_packages(),
    requires=["numpy"],
    install_requires=["numpy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    ext_modules=[
        Extension(
            "cougar.rolling",
            ["cougar/cext/rolling.c"],
            include_dirs=["cougar/cext", np.get_include()],
            extra_compile_args=["-O2"],
        )
    ],
)
