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
from springcloudstream.grpc.message import Message, MessageHeaders

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))


class MessageTest(unittest.TestCase):
    def test_default(self):
        message = Message("hello")
        self.assertEquals("hello", message.payload)
        self.assertIsNotNone(message.headers)

    def test_bytes_payload(self):
        message = Message(bytearray("hello", 'utf-8'))
        self.assertEquals("hello", str(message.payload))

    def test_bool_payload(self):
        message = Message(True)
        self.assertEquals(True, message.payload)

    def test_int_payload(self):
        message = Message(123)
        self.assertEquals(123, message.payload)

    def test_long_payload(self):
        message = Message(long(123))
        self.assertEquals(long(123), message.payload)

    def test_float_payload(self):
        message = Message(123.45)
        self.assertEquals(123.45, message.payload)

    def test_with_headers(self):
        headers = MessageHeaders({'foo': 'bar'})
        message = Message("hello", headers)
        self.assertEquals('bar', message.headers['foo'])

    def test_unsupported_header_types(self):
        try:
            message = Message("hello", {'foo': 'bar'})
            self.fail('Should raise an error')
        except RuntimeError:
            pass

    def test_unsupported_payload_types(self):
        try:
            message = Message({'foo': 'bar'})
            self.fail('Should raise an error')
        except RuntimeError:
            pass
