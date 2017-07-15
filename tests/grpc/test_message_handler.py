__copyright__ = '''
Copyright 2017 the original author or authors.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
__author__ = 'David Turanski'

import os
import sys
import unittest
from springcloudstream.grpc.message import Message, MessageHeaders,__convert_from_generic__,__convert_to_generic__,\
    FLOAT_MIN_VALUE,FLOAT_MAX_VALUE

import springcloudstream.grpc.message_pb2
from springcloudstream.grpc.message_pb2 import Generic

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
    long = int
    from inspect import getfullargspec
else:
    from inspect import getargspec as getfullargspec

class MessageHandlerTest(unittest.TestCase):

    def test_default(self):

        def function(payload, headers):
            pass

        sig = getfullargspec(function)
        self.assertEqual(2, len(sig.args))


