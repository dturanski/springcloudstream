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
import struct
from tests.tcptest.testutils import TcpTestCase


def random_data(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

class BaseTestCases:
    class TestTcpUpperBase(TcpTestCase):

        def test_ping(self):
            try:
                sock = self.create_socket(9998)
                sock.sendall("ping\n".encode('utf-8'))
                result = sock.recv(80)
                result = result.decode('utf-8')
                self.assertEqual('alive', result.rstrip())
            finally:
                sock.close()

        def test_random_data(self):
            header_len = self.__class__.HEADER_LEN

            SZ1, SZ2, SZ3 = 10, 1025, 2051
            if (header_len == 1):
                SZ1, SZ2, SZ3 = 10, 81, 127

            try:
                sock = self.create_socket()
                # Connect to server and send data
                for i in range(10):
                    self.sendAndRecieve(sock, random_data(SZ1))
                    self.sendAndRecieve(sock, random_data(SZ2))
                    self.sendAndRecieve(sock, random_data(SZ3))

            finally:
                sock.close()

        def sendAndRecieve(self, sock, data):
            header_len = self.__class__.HEADER_LEN
            format = self.__class__.FORMAT
            ba = bytearray(struct.pack(format, len(data)))
            ba.extend(data.encode('utf-8'))

            sock.sendall(ba)
            # Receive data from the server and shut down
            # Different for Python 3
            # str(sock.recv(1024),"utf-8")
            received = sock.recv(len(data) + header_len)
            l = struct.unpack(format, received[:header_len])[0]
            result = received[header_len:]
            self.assertEqual(len(data), l)
            self.assertEqual(data.upper().encode('utf-8'), result)


class TestTcpL2(BaseTestCases.TestTcpUpperBase):
    SERVER_NAME = 'tcp_upper_hl2.py'
    FORMAT = '!H'
    HEADER_LEN = 2


class TestTcpL4(BaseTestCases.TestTcpUpperBase):
    SERVER_NAME = 'tcp_upper_hl4.py'
    FORMAT = '!l'
    HEADER_LEN = 4


class TestTcpL1(BaseTestCases.TestTcpUpperBase):
    SERVER_NAME = 'tcp_upper_hl1.py'
    FORMAT = 'b'
    HEADER_LEN = 1


class TestTcpBinary(TcpTestCase):
    SERVER_NAME = 'tcp_binary.py'

    def test(self):
        try:
            sock = self.create_socket()
            data = struct.pack('!if', 2, 3.0)
            data = struct.pack('!H', len(data)) + data
            sock.sendall(bytearray(data))
            received = sock.recv(1024)
            l = struct.unpack('!H', received[:2])[0]
            result = struct.unpack('f', received[2:])[0]
            self.assertEqual(result, 6.0)
        finally:
            sock.close()


if __name__ == 'main':
    unittest.main()
