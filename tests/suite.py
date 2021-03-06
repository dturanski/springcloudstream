__copyright__ = """
Copyright 2016 the original author or authors.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

import tests.tcptest.suite
import tests.grpctest.suite
test_loader = unittest.defaultTestLoader
test_suite = test_loader.discover('.')
runner=unittest.TextTestRunner()
runner.run(test_suite)
