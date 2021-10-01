#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["pandas==1.3.3", "mecha==0.5.0", "docopt==0.6.2"]

setup(
    author="Manas Mengle",
    author_email="manmenonsense@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="A CLI application to generate give commands for shulker boxes full of items for litematica projects. Used by the lazy survival player :).",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="litematica_command_gen",
    name="litematica_command_gen",
    packages=find_packages(
        include=["litematica_command_gen", "litematica_command_gen.*"]
    ),
    url="https://github.com/appcreatorguy/litematica_command_gen",
    version="0.1.0",
    zip_safe=False,
    package_data={
        "": ["data/*"],
    },
)
