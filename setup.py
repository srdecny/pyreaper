# coding: utf-8

from __future__ import with_statement, print_function, absolute_import

from setuptools import setup, find_packages, Extension
from distutils.version import LooseVersion

import numpy as np
import os
from glob import glob
from os.path import join
from sys import platform


try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext
    cmdclass = {'build_ext': build_ext}
except ImportError:
    cythonize = None
    cmdclass = {}

# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions


COMPILE_ARGS = [
    "-std=c++11",
    "-funsigned-char",
]
if os.name != "nt":
    COMPILE_ARGS.append("-Wno-register")
    COMPILE_ARGS.append("-Wno-unused-function")
    COMPILE_ARGS.append("-Wno-unused-local-typedefs")

if platform.startswith("darwin"):
    COMPILE_ARGS.append("-stdlib=libc++")
    COMPILE_ARGS.append("-mmacosx-version-min=10.7")




ext = '.pyx'
compiler_directives = {"language_level": 3, "embedsignature": True}


# REAPER source location
src_top = join("lib", "REAPER")

src = glob(join(src_top, "core", "*.cc")) \
    + glob(join(src_top, "epoch_tracker", "*.cc"))
print(src)


# define core cython module
extensions = [Extension(
    name="pyreaper.creaper",
    sources=[join("pyreaper", "creaper" + ext)] + src,
    include_dirs=[np.get_include(), join(os.getcwd(), "lib", "REAPER")],
    extra_compile_args=COMPILE_ARGS,
    language="c++",
)]


CYTHONIZE = bool(int(os.getenv("CYTHONIZE", 0))) and cythonize is not None

if CYTHONIZE:
    compiler_directives = {"language_level": 3, "embedsignature": True}
    extensions = cythonize(extensions, compiler_directives=compiler_directives)
else:
    extensions = no_cythonize(extensions)

with open('README.md', 'r') as fd:
    long_description = fd.read()

setup(
    name='pyreaper',
    version='0.0.9-dev',
    description='A python wrapper for REAPER (Robust Epoch And Pitch EstimatoR)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ryuichi Yamamoto',
    author_email='zryuichi@gmail.com',
    url='https://github.com/r9y9/pyreaper',
    license='MIT',
    packages=find_packages(),
    ext_modules=extensions,
    cmdclass=cmdclass,
    install_requires=[
        'numpy >= 1.8.0',
    ],
    tests_require=['nose', 'coverage'],
    extras_require={
        'test': ['nose', 'scipy'],
    },
    classifiers=[
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
    ],
    keywords=["REAPER"]
)
