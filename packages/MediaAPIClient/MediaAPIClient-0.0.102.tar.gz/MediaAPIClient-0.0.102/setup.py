from setuptools import setup, find_packages

setup(
    name='MediaAPIClient',
    version='0.0.102',
    packages=find_packages(),
    install_requires=[
        'pydantic~=1.8.2',
        'setuptools~=65.5.1',
        'requests~=2.26.0',
    ],
    author='Semyon Shilovskiy',
    description='A library for working with REST API of CAG',
    url='https://github.com/Dragon4231/cag_library',
)