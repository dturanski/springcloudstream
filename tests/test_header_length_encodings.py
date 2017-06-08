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

import socket
import sys
import random
import string
import os
import unittest
import subprocess
import signal
import time
import struct

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

skip_tests = os.environ.get('SKIP_TESTS', False)

HOST, PORT = "localhost", 9999

PYTHON3 = sys.version_info >= (3, 0)

PY_COMMAND = 'python'
if PYTHON3:
    PY_COMMAND = 'python3'

def random_data(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


class BaseTestCases:
    @unittest.skipIf(skip_tests, 'tests skipped')
    class TestTcpUpperBase(unittest.TestCase):

        @classmethod
        def setUpClass(cls, server):
            print("starting %s" % server)
            cls.process = subprocess.Popen(
                "%s %s" %(PY_COMMAND, server),
                shell=True, preexec_fn=os.setsid
            )
            time.sleep(1.0)

        @classmethod
        def tearDownClass(cls):
            try:
                os.killpg(cls.process.pid, signal.SIGTERM)
            except:
                print("ERROR: Unable to kill PID %d" % cls.process.pid)

        def test_ping(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((HOST, 9998))
                sock.sendall("ping\n".encode('utf-8'))
                result = sock.recv(80)
                result = result.decode('utf-8')
                self.assertEqual('alive', result.rstrip())
            finally:
                sock.close()

        def test_random_data(self):
            # Create a socket (SOCK_STREAM means a TCP socket)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            header_len = self.__class__.HEADER_LEN

            SZ1,SZ2,SZ3 = 10, 1025,2051
            if (header_len == 1):
                SZ1, SZ2, SZ3 = 10, 81, 127


            try:
                sock.connect((HOST, PORT))
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
    SERVER = 'servers/tcp_upper_hl2.py'
    FORMAT = '!H'
    HEADER_LEN = 2

    @classmethod
    def setUpClass(cls):
        BaseTestCases.TestTcpUpperBase.setUpClass(TestTcpL2.SERVER)

    @classmethod
    def tearDownClass(cls):
        BaseTestCases.TestTcpUpperBase.tearDownClass()

class TestTcpL4(BaseTestCases.TestTcpUpperBase):
    SERVER = 'servers/tcp_upper_hl4.py'
    FORMAT = '!L'
    HEADER_LEN = 4

    @classmethod
    def setUpClass(cls):
        BaseTestCases.TestTcpUpperBase.setUpClass(TestTcpL4.SERVER)

    @classmethod
    def tearDownClass(cls):
        BaseTestCases.TestTcpUpperBase.tearDownClass()

class TestTcpL1(BaseTestCases.TestTcpUpperBase):
    SERVER = 'servers/tcp_upper_hl1.py'
    FORMAT = 'b'
    HEADER_LEN = 1

    @classmethod
    def setUpClass(cls):
        BaseTestCases.TestTcpUpperBase.setUpClass(TestTcpL1.SERVER)

    @classmethod
    def tearDownClass(cls):
        BaseTestCases.TestTcpUpperBase.tearDownClass()