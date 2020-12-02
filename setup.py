#!/usr/bin/env python
import os

"""The setup script."""

from setuptools import setup, find_packages

os.system('rm -rf dist')

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pytest', 'cmd2', 'gnureadline', 'pydicom', 'pandas', 'numpy', 'SimpleITK']

setup_requirements = []

test_requirements = []

version = '0.7.0'

setup(
    author="Ralph Brecheisen",
    author_email='ralph.brecheisen@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of command-line tools",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='caipirinha_cmdtools',
    name='caipirinha_cmdtools',
    packages=find_packages(include=['caipirinha_cmdtools', 'caipirinha_cmdtools.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rbrecheisen/caipirinha_cmdtools',
    version=version,
    zip_safe=False,
)
