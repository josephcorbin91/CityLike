"""Setup.py for ProsperAPI Flask project"""

from os import path, listdir
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

HERE = path.abspath(path.dirname(__file__))
__version__ = '0.9.0'
__package_name__ = 'citylake'

def include_all_subfiles(*args):
    """Slurps up all files in a directory (non recursive) for data_files section

    Note:
        Not recursive, only includes flat files

    Returns:
        (:obj:`list` :obj:`str`) list of all non-directories in a file

    """
    file_list = []
    for path_included in args:
        local_path = path.join(HERE, path_included)

        for file in listdir(local_path):
            file_abspath = path.join(local_path, file)
            if path.isdir(file_abspath):        #do not include sub folders
                continue
            file_list.append(path_included + '/' + file)

    return file_list

class PyTest(TestCommand):
    """PyTest cmdclass hook for test-at-buildtime functionality

    http://doc.pytest.org/en/latest/goodpractices.html#manual-integration

    """
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            '-rx',
            'tests',
            '--cov={}/'.format(__package_name__),
            '--cov-report=term-missing'
        ]    #load defaults here

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest_commands = []
        try:    #read commandline
            pytest_commands = shlex.split(self.pytest_args)
        except AttributeError:  #use defaults
            pytest_commands = self.pytest_args
        errno = pytest.main(pytest_commands)
        exit(errno)

setup(
    name=__package_name__,
    author='Joseph Corbin',
    author_email='TODO',
    url='https://github.com/josephcorbin91/CityLike',
    download_url='https://github.com/josephcorbin91/CityLike/tarball/v' + __version__,
    version=__version__,
    license='TODO',
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ],
    keywords='seattle d4d data gov rest',
    packages=find_packages(),
    data_files=[
        ('docs', include_all_subfiles('docs')),
        ('tests', include_all_subfiles('tests')),
        ('scripts', include_all_subfiles('scripts'))
    ],
    package_data={
        '': ['LICENSE', 'README.rst'],
        __package_name__:[
            'my_config.cfg'
        ]
    },
    install_requires=[
        'pandas~=0.20.2',
        'sodapy~=1.4.3',
        'requests~=2.18.1',
        'plumbum~=1.6.3'
    ],
    tests_require=[
        'pytest~=3.0.0',
        'pytest_cov~=2.4.0'
    ],
    cmdclass={
        'test':PyTest
    }
)
