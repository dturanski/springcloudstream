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
from springcloudstream.grpc.message import MessageHeaders

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

class MessageHeadersTest(unittest.TestCase):

    def test_default(self):
        headers = MessageHeaders()
        self.assertIsNotNone(headers['id'])
        self.assertIsNotNone(headers['timestamp'])

    def test_basic(self):
        headers = MessageHeaders()
        headers['foo']='bar'
        headers['num']=13
        self.assertEquals(13,headers['num'])
        self.assertEquals('bar',headers['foo'])

    def test_immutable_values(self):
        headers = MessageHeaders()
        try:
            headers['id']='new id'
            self.fail('should raise KeyError')
        except KeyError:
            self.assertEquals('"key \'id\' cannot be updated"', str(sys.exc_info()[1]))
        try:
            headers['timestamp']= 0
            self.fail('should raise KeyError')
        except KeyError:
            self.assertEquals('"key \'timestamp\' cannot be updated"', str(sys.exc_info()[1]))
        try:
            del headers['id']
            self.fail('should raise KeyError')
        except KeyError:
            self.assertEquals('"key \'id\' cannot be deleted"', str(sys.exc_info()[1]))
        try:
            del headers['timestamp']
            self.fail('should raise KeyError')
        except KeyError:
            self.assertEquals('"key \'timestamp\' cannot be deleted"', str(sys.exc_info()[1]))


    def test_supported_types(self):
        headers = MessageHeaders()
        headers['str'] = 'hello'
        headers['bytes'] = bytearray('world','utf-8')
        headers['float'] = 123.0
        headers['int'] = 123
        headers['long'] = long(123)
        headers['bool'] = True

    def test_unsupported_types(self):
        headers = MessageHeaders()
        try:
            headers['none'] = None
            self.fail('should raise RuntimeError')
        except RuntimeError:
           self.assertEquals("<type 'NoneType'> is an unsupported type", str(sys.exc_info()[1]))
        try:
            headers['dict'] = {'a':'a'}
            self.fail('should raise RuntimeError')
        except RuntimeError:
           pass

        try:
            headers['list'] = [1,2,3]
            self.fail('should raise RuntimeError')
        except RuntimeError:
           pass
