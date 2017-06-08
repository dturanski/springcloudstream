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


sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))



skip_tests = os.environ.get('SKIP_TESTS', False)

HOST, PORT = "localhost", 9999



def random_data(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size)) + '\n'


@unittest.skipIf(skip_tests, 'tests skipped')
class TestTcp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(
            'python servers/tcp_upper.py',
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
            self.assertEqual('alive',result.rstrip())
        finally:
            sock.close()


    def test_random_data(self):
        # Create a socket (SOCK_STREAM means a TCP socket)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((HOST, PORT))
            # Connect to server and send data
            for i in range(10):
                self.sendAndRecieve(sock, random_data(10))
                self.sendAndRecieve(sock, random_data(1025))
                self.sendAndRecieve(sock, random_data(2048))

        finally:
            sock.close()

    def test_multi_data(self):
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall("hello\nworld\n".encode('utf-8'))
            result = sock.recv(1024)
            result = result.decode('utf-8')

            self.assertEqual('HELLO',result.rstrip())
            result = sock.recv(1024)
            result = result.decode('utf-8')
            self.assertEqual('WORLD', result.rstrip())
        finally:
            sock.close()

    def sendAndRecieve(self, sock, data):
        sock.sendall(data.encode('utf-8'))
        # Receive data from the server and shut down
        # Different for Python 3
        # str(sock.recv(1024),"utf-8")
        result =  sock.recv(len(data))
        result = result.decode('utf-8')
        self.assertEqual(data.upper(), result)


