#!/usr/bin/env python3

"""
The package's information.
"""

from setuptools import setup  # type: ignore
from fastimer import constants


with open("README.md", encoding="utf-8-sig") as readme_file:
    long_description = readme_file.read()

setup(
    name="fastimer",
    version=constants.VERSION,
    description="A simple CLI tool to track food you consume",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vkostyanetsky/Fastimer",
    license="MIT",
    python_requires=">=3.10",
    packages=["fastimer"],
    install_requires=[
        "pyyaml~=6.0.1",
        "click~=8.1.6",
    ],
    entry_points={"console_scripts": ["fastimer=fastimer.app:cli"]},
    author="Vlad Kostyanetsky",
    author_email="vlad@kostyanetsky.me",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    keywords="fasting fast",
)
