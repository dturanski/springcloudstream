"""
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
"""
import unittest
import sys
import os
from subprocess import PIPE, Popen

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

skip_tests = os.environ.get('SKIP_TESTS', False)


@unittest.skipIf(skip_tests, 'tests hang with setup (hijacking stdin stdout)')
class TestEncoders(unittest.TestCase):

    def test_echo(self):
        cmd = 'echo.py'
        input = 'hello\r\n'
        self.do_test(cmd, input, iterations=100)

    def test_echo_lf(self):
        cmd = 'echo_lf.py'
        input = 'hello\n'
        self.do_test(cmd, input, iterations=100)

    def do_test(self, cmd, input, iterations=1):
        print(sys.version_info)
        dir = os.getcwd()
        if not dir.endswith('tests'):
            dir = dir + "/tests"

        cmd = dir + '/' + cmd

        self.proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
        input = input.encode('utf-8')
        for i in range(iterations):
            self.proc.stdin.write(input)
            self.proc.stdin.flush()
            data = self.proc.stdout.readline()
            self.assertEqual(input, data)

    def test_echo_binary(self):
        cmd = 'echo_binary.py'
        input = 'hel\rlo\n\x1a'
        iterations = 1
        dir = os.getcwd()
        if not dir.endswith('tests'):
            dir = dir + "/tests"

        cmd = dir + '/' + cmd

        self.proc = Popen(cmd, stdout=PIPE, stdin=PIPE)
        input = input.encode('utf-8')
        for i in range(iterations):
            self.proc.stdin.write(input)
            self.proc.stdin.flush()

            buffer = []
            while True:
                data = self.proc.stdout.read(1)
                buffer.append(data)
                if (data == '\x1a'):
                    break

            self.assertEqual(input, ''.join(buffer))




    def tearDown(self):
        self.proc.terminate()

if __name__ == '__main__':
    unittest.main()
