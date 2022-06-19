#!/usr/bin/env python
import re, os, codecs
import sys
import unittest
from setuptools import setup, find_packages

if __package__:
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
else:
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def load_projectrc(projectrc_filepath):
    """
    Load the values of .projectrc file
    """
    from dotenv import dotenv_values
    return dotenv_values(projectrc_filepath)


env_vars = {}
projectrc_file = os.path.join(CURRENT_DIR, '.projectrc')

# inside of a docker the name of folder is app
PROJECT_NAME = os.path.basename(CURRENT_DIR).replace('_', '-')

if not CURRENT_DIR[-1]=='/':
    CURRENT_DIR += '/'

if os.path.exists(projectrc_file):
    env_vars = load_projectrc(projectrc_file)

# print('exit')
# print(env_vars['APP_NAME'])
# sys.exit(1)


def read(*parts):
    return codecs.open(os.path.join(CURRENT_DIR, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^APP_VERSION = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def unit_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir='tests/unit', pattern='test_*.py', top_level_dir='./')
    return test_suite


# Module requirements
install_requires = read('requirements.txt').split('\n')

setup(
    name=env_vars['APP_NAME'],
    version=env_vars['APP_VERSION'],
    author=env_vars['APP_AUTHOR'],
    author_email=env_vars['APP_AUTHOR_EMAIL'],
    description=env_vars['APP_DESCRIPTION'],
    long_description=read('README.md'),
    # UserWarning: Unknown distribution option: 'long_description_content_type'
    # long_description_content_type="text/markdown",
    url=env_vars['APP_REPOSITORY'],
    packages=find_packages(exclude=("./tests/*", "./examples/*", "./samples/*", "./docs/*")),
    data_files=[("./", ["./app.py", "./boot.py", "./server.py"])],
    include_package_data=True,
    install_requires=install_requires,
    test_suite='setup.unit_test_suite',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
