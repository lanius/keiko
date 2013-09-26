import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

import keiko


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main('keiko tests --pep8 --flakes')
        sys.exit(errno)


install_requires = ['flask']


if sys.version_info < (2, 7):
    install_requires.append('argparse')


setup(
    name='keiko',
    version=keiko.__version__,
    description='keiko is Python and Web API clients for Keiko-chan.',
    long_description=open('README.rst').read(),
    author='lanius',
    author_email='lanius@nirvake.org',
    url='https://github.com/lanius/keiko/',
    packages=['keiko'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'keiko = keiko.app:main',
        ],
    },
    install_requires=install_requires,
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Japanese',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3'
    ),
    tests_require=['mock', 'pytest', 'pytest-pep8', 'pytest-flakes'],
    cmdclass = {'test': PyTest},
)
