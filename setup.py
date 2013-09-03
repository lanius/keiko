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
        pytest.main(self.test_args)


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
    install_requires=['flask'],
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Japanese',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3'
    ),
    tests_require=['pytest', 'mock'],
    cmdclass = {'test': PyTest},
)