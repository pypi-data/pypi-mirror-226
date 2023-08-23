from setuptools import setup, find_packages

setup(
    name='Interphase',
    version='0.0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
    packages=find_packages(
        # All keyword arguments below are optional:
        where='Interphase',  # '.' by default
        include=['*'],  # ['*'] by default
        exclude=[],  # empty by default
    ),
    entry_points={
        'console_scripts': [
            'cli-name = mypkg.mymodule:some_func',
        ]
    }
)