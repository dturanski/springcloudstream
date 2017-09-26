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
import optparse

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

from springcloudstream.tcp.stream import options_parser


class OptionsTest(unittest.TestCase):
    def test_default_options(self):
        options, args = options_parser.parse([])

        self.assertEquals(2048, options.buffer_size)
        self.assertEquals('LF', options.encoder)
        self.assertEqual(False, options.debug)
        self.assertEqual(None, options.port)
        self.assertEqual(None, options.monitor_port)
        self.assertEqual('utf-8', options.char_encoding)

    def test_help(self):
        try:
            opts = options_parser.parse(['-h'])
        except SystemExit:
            pass

    def test_validate_encoder(self):
        try:
            opts, args = options_parser.parse(['-e foo'], validate=True)

            self.fail("should not except this value")
        except SystemExit:
            pass

    def test_validate_port_not_defined(self):
        try:
            options_parser.parse([], validate=True)
            self.fail("should not except these values")
        except SystemExit:
            pass

    def test_validate_ports_not_equal(self):
        try:
            options_parser.parse(['--port', '1234', '--monitor-port', '1234'], validate=True)
            self.fail("should not except these values")
        except SystemExit:
            pass

    def test_encoder(self):
        options, args = options_parser.parser.parse_args(['--port', '9999', '--host', 'localhost', '--monitor-port', '9998', '--debug', '--encoder', 'CRLF'])
        self.assertEquals('CRLF',options.encoder)

    def test_unparsed_options(self):
        opts = optparse.Values()
        original_args = ['--port', '1234', '--monitor-port', '8888', '--', '--function', 'foo.bar', '--package',
                         'mypackage']
        opts, args = options_parser.parse(original_args)
        tcp_args = original_args[:original_args.index('--')]
        self.assertTrue(tcp_args == ['--port', '1234', '--monitor-port', '8888'])
        self.assertTrue(args == ['--function', 'foo.bar', '--package', 'mypackage'])


        original_args = ['--port', '1234', '--monitor-port', '8888', 'function', 'foo.bar', 'package',
                         'mypackage']
        opts, args = options_parser.parse(original_args)
        self.assertTrue(args == ['function', 'foo.bar', 'package', 'mypackage'])
        tcp_args = [x for x in original_args if x not in args]
        self.assertTrue(tcp_args == ['--port', '1234', '--monitor-port', '8888'])

    def test_validate_char_encoder(self):
        try:
            opts, args = options_parser.parse(['-p', '1234', '-c', 'utf-999'], validate=True)
            self.fail("should not except these values")
        except SystemExit:
            pass


if __name__ == 'main':
    unittest.main()
