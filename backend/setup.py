"""Backend python package configuration."""

from setuptools import find_packages, setup

setup(
    name='backend',
    version='0.0.1',
    packages=find_packages(),
    package_data={'': ["token/*.json"]},
    include_package_data=True,
    install_requires=[
        'google-api-python-client',
        'oauth2client',
        'httplib2',
        'arrow',
        'Flask',
        'html5validator',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
    ],
    python_requires='>=3.6',
)