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

import os, sys
import unittest
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

from springcloudstream.stream import Options

class OptionsTest(unittest.TestCase):

    def test_default_options(self):
        opts = Options([])
        options = opts.options

        self.assertEquals(2048, options.buffer_size)
        self.assertEquals('LF', options.encoder)
        self.assertEqual(False,options.debug)
        self.assertEqual(None, options.port)
        self.assertEqual(None, options.monitor_port)
        self.assertEqual('utf-8', options.char_encoding)

    def test_help(self):
        try:
            opts = Options(['-h'])
        except SystemExit:
            pass

    def test_validate_encoder(self):
        try:
            opts = Options(['-e foo'])
            self.fail("should not except this value")
        except SystemExit:
            pass

    def test_validate_port_not_defined(self):
        try:
            opts = Options([])
            opts.validate()
            self.fail("should not except these values")
        except SystemExit:
            pass

    def test_validate_ports_not_equal(self):
        try:
            opts = Options(['--port','1234','--monitor-port','1234'])
            opts.validate()
            self.fail("should not except these values")
        except SystemExit:
            pass

    def test_validate_char_encoder(self):
        try:
            opts = Options(['-p', '1234', '-c', 'utf-999'])
            opts.validate()
            self.fail("should not except these values")
        except SystemExit:
            pass

if __name__ == 'main':
    unittest.main()
