from setuptools import setup, find_packages

setup(
    name='fastmodels',
    version='0.1.8',
    description='A command-line interface for interacting with FastModel product and services.',
    packages=find_packages(),
    install_requires=[
        'jsonschema', 'requests'
    ],
    entry_points={
        'console_scripts': [
            'fastmodels=fastmodels.cli:main',
        ],
    },
)
