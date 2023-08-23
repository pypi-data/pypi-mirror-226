# -*- coding: utf-8 -*-
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="codeboxcli",
    version="v23.8.4",
    description='CLI for Saving and Sharing Code Snippets',
    author='Marc Orfila Carreras',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "tabulate"
    ],
    entry_points={
        "console_scripts": [
            "codebox=codeboxcli.__main__:cli",
        ],
    },
)
