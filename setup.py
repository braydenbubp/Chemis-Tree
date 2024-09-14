from setuptools import setup, find_packages

setup(
    name='chemapp',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'rdkit-pypi==2024.3.5',
    ],
)
