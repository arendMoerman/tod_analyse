import os
import pathlib

from setuptools import setup

setup(
    name='tod_analyse',
    version='1.0.0',
    author="Arend Moerman",
    install_requires = ["numpy", "matplotlib", "scipy", "astropy", "xarray", "tqdm"],
    package_dir = {'': '.'},
    packages=['tod_analyse'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.8',
)
