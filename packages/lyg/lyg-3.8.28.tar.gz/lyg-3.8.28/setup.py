import os
import distro
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install

setup(
    name="lyg",
    version="3.8.28",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows"
    ],
    author="LYG.AI",
    author_email="team@lyg.ai",
    url="https://lyg.ai",
)

