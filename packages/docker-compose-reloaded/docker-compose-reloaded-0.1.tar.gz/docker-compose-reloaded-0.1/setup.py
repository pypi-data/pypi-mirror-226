#!/usr/bin/python3

from setuptools import find_packages, setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name='docker-compose-reloaded',
    version='0.1',
    author='TheClockTwister',
    description='A python CLI tool to update stacks on event triggers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['click', 'colorama', 'paho-mqtt'],
    entry_points={  # CLI scripts
        'console_scripts': [
            'dcr = docker_compose_reloaded:cli',
        ],
    },
)
