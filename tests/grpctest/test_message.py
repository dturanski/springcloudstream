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

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

from springcloudstream.portability import long
import springcloudstream.proto.message_pb2
from springcloudstream.grpc.message import Message, MessageHeaders, __convert_from_generic__, __convert_to_generic__, \
    FLOAT_MIN_VALUE, FLOAT_MAX_VALUE
from springcloudstream.proto.message_pb2 import Generic


class MessageTest(unittest.TestCase):
    def test_default(self):
        message = Message("hello")
        self.assertEqual("hello", message.payload)
        self.assertIsNotNone(message.headers)

    def test_bytes_payload(self):
        message = Message(bytes('hello'.encode('utf-8')))
        self.assertEqual("hello", message.payload.decode('utf-8'))

    def test_bool_payload(self):
        message = Message(True)
        self.assertEqual(True, message.payload)

    def test_int_payload(self):
        message = Message(123)
        self.assertEqual(123, message.payload)

    def test_long_payload(self):
        message = Message(long(123))
        self.assertEqual(long(123), message.payload)

    def test_float_payload(self):
        message = Message(123.45)
        self.assertEqual(123.45, message.payload)

    def test_with_headers(self):
        headers = MessageHeaders({'foo': 'bar'})
        message = Message("hello", headers)
        self.assertEqual('bar', message.headers['foo'])

    def test_unsupported_header_types(self):
        try:
            message = Message("hello", {'foo': 'bar'})
            self.fail('Should raise an error')
        except TypeError:
            pass

    def test_unsupported_payload_types(self):
        try:
            message = Message({'foo': 'bar'})
            self.fail('Should raise an error')
        except TypeError:
            pass

    def test_generic(self):

        def do_test(expected):
            actual = Generic()
            __convert_to_generic__(actual,expected)
            val = __convert_from_generic__(actual)
            self.assertEqual(expected ,val)

        do_test(123.4)
        do_test("hello")
        do_test(bytes("hello".encode('utf-8')))
        do_test(True)
        do_test(123)
        do_test(FLOAT_MIN_VALUE/2.0)
        do_test(FLOAT_MAX_VALUE + 0.1)

    def test_from_protobuf_message(self):
        pb_message = springcloudstream.proto.message_pb2.Message()
        pb_message.payload.string = 'greetings'
        pb_message.headers['id'].string ='id1'
        pb_message.headers['timestamp'].long = long(9999999)
        pb_message.headers['str'].string = 'hello'
        pb_message.headers['bytes'].bytes = bytes('world'.encode('utf-8'))
        pb_message.headers['float'].float = 123.0
        pb_message.headers['int'].int = 123
        pb_message.headers['long'].long = long(123)
        pb_message.headers['bool'].bool = True

        message = Message.__from_protobuf_message__(pb_message)
        self.assertEqual('greetings',message.payload)
        self.assertEqual('id1',message.headers['id'])
        self.assertEqual(9999999,message.headers['timestamp'])
        self.assertEqual('hello',message.headers['str'])
        self.assertEqual(bytes('world'.encode('utf-8')), message.headers['bytes'])
        self.assertEqual(123.0, message.headers['float'])
        self.assertEqual(123, message.headers['int'])
        self.assertEqual(long(123), message.headers['long'])
        self.assertEqual(True, message.headers['bool'])