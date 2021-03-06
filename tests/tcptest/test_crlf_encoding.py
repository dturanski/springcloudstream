__copyright__ = """
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

import random
import string
import unittest

from tests.tcptest.base import TcpTestCase


def random_data(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size)) + '\r\n'


class TestTcp(TcpTestCase):
    SERVER_NAME = 'tcp_upper_crlf.py'

    def test_random_data(self):

        try:
            sock = self.create_socket(host='localhost')
            # Connect to server and send data
            for i in range(10):
                self.sendAndRecieve(sock, random_data(10))
                self.sendAndRecieve(sock, random_data(1025))
                self.sendAndRecieve(sock, random_data(2048))

        finally:
            sock.close()

    def test_multi_line(self):
        # Create a socket (SOCK_STREAM means a TCP socket)
        try:
            sock = self.create_socket(host='localhost')
            sock.sendall("hello\r\nworld\r\n".encode('utf-8'))
            result = sock.recv(1024)
            result = result.decode('utf-8')

            self.assertEqual('HELLO', result.rstrip())
            result = sock.recv(1024)
            result = result.decode('utf-8')
            self.assertEqual('WORLD', result.rstrip())
        finally:
            sock.close()

    def sendAndRecieve(self, sock, data):
        sock.sendall(data.encode('utf-8'))
        result = sock.recv(len(data))
        result = result.decode('utf-8')
        self.assertEqual(data.upper(), result)


if __name__ == 'main':
    unittest.main()
