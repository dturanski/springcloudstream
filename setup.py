#!/usr/bin/env python

from setuptools import setup, find_packages
import unittest

def setup_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(name='springcloudstream',
      version='1.1.6',
      test_suite='__main__.setup_test_suite',
      description='A package to support invocation of remote Python applications via Spring Cloud Stream',
      author='David Turanski',
      author_email='dturanski@pivotal.io',
      url = 'https://github.com/dturanski/springcloudstream',
      packages=find_packages(exclude=['tests', 'tests.*', 'stdiotests','stdiotests.*']),
      license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: Apache Software License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
      install_requires=['grpcio'],  # external packages as dependencies
      ext_modules=[],
      tests_require=['mock', 'unittest2'],
      )
