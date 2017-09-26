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

import array
import os
import random
import string
import struct
import sys
import unittest

from tests.tcptest.base import TcpTestCase

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

from springcloudstream.tcp.messagehandler import StxEtxHandler, rindex, split_array


def random_data(size):
    random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    return encode(random_str)


def encode(s):
    ba = bytearray(s, 'utf-8')
    bytes = array.array('B', ba)
    bytes.insert(0, 2)
    bytes.append(3)
    return bytes


class TestBasicProtocol(unittest.TestCase):
    def test(self):
        bytes = encode('hello')
        self.assertEqual(StxEtxHandler.STX, bytes[0])
        bytes = encode('hello') + encode('world')
        self.assertEqual(StxEtxHandler.ETX, bytes[-1])

        etx_pos = rindex(bytes, StxEtxHandler.ETX)
        self.assertEqual(etx_pos, len(bytes) - 1)
        stx_pos = bytes.index(StxEtxHandler.STX)
        self.assertEqual(0, stx_pos)
        splits = split_array(bytes, StxEtxHandler.ETX)

        h = bytearray(splits[0][1:]).decode('utf-8')
        w = bytearray(splits[1][1:]).decode('utf-8')

        self.assertEqual('hello', h)
        self.assertEqual('world', w)

    def test_split_array(self):
        lst = array.array('I', range(6))
        splits = split_array(lst, 3)
        self.assertEqual(array.array('I', [0, 1, 2]), splits[0])
        self.assertEqual(array.array('I', [4, 5]), splits[1])

        splits = split_array(lst, 5)
        self.assertEqual(1, len(splits), splits)
        self.assertEqual(array.array('I', [0, 1, 2, 3, 4]), splits[0])

        splits = split_array(lst, 0)
        self.assertEqual(1, len(splits), splits)
        self.assertEqual(array.array('I', [1, 2, 3, 4, 5]), splits[0])

        splits = split_array(lst, 8)
        self.assertEqual(1, len(splits), splits)
        self.assertEqual(array.array('I', [0, 1, 2, 3, 4, 5]), splits[0])

        lst = array.array('I', [1, 2, 3, 0, 4, 5, 6, 0, 7, 8, 9, 0])
        splits = split_array(lst, 0)
        self.assertEqual(3, len(splits), splits)
        self.assertEqual(array.array('I', [1, 2, 3]), splits[0])
        self.assertEqual(array.array('I', [4, 5, 6]), splits[1])
        self.assertEqual(array.array('I', [7, 8, 9]), splits[2])


class TestTcp(TcpTestCase):
    SERVER_NAME = 'tcp_upper_stxetx.py'

    def test_random_data(self):
        try:
            sock = self.create_socket()
            for i in range(10):
                self.sendAndRecieve(sock, random_data(10))
                self.sendAndRecieve(sock, random_data(1025))
                self.sendAndRecieve(sock, random_data(2048))

        finally:
            sock.close()

    def test_multi_data(self):
        try:
            # Connect to server and send data
            sock = self.create_socket()
            sock.sendall(bytearray(chr(2) + 'hello' + chr(3) + chr(2) + 'world' + chr(3), 'utf-8'))
            result = sock.recv(1024)
            result = result.decode('utf-8')
            self.assertEqual('\x02HELLO\x03', result)
            result = sock.recv(1024)
            result = result.decode('utf-8')
            self.assertEqual('\x02WORLD\x03', result)
        finally:
            sock.close()

    def sendAndRecieve(self, sock, data):
        sock.sendall(data)
        # Receive data from the server and shut down
        # Different for Python 3
        # str(sock.recv(1024),"utf-8")
        result = sock.recv(len(data))
        result = result.decode('utf-8')
        self.assertEqual(bytearray(data).decode('utf-8').upper(), result)


class TestTcpBinary(TcpTestCase):
    SERVER_NAME = 'tcp_binary_stxetx.py'

    def test(self):
        try:
            sock = self.create_socket()
            data = bytearray(struct.pack('!if', 2, 3.0))
            data.insert(0, 2)
            data.append(3)
            sock.sendall(data)
            received = sock.recv(1024)
            result = struct.unpack('f', received[1:-1])[0]
            self.assertEqual(result, 6.0)
        finally:
            sock.close()


if __name__ == 'main':
    unittest.main()
