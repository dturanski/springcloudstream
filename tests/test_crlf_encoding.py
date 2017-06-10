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


HOST, PORT = "localhost", 9999

PYTHON3 = sys.version_info >= (3, 0)

PY_COMMAND = 'python'
if PYTHON3:
    PY_COMMAND = 'python3'

def random_data(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size)) + '\r\n'

def servers_root():
    if (os.getcwd().endswith('springcloudstream')):
        return './tests'
    elif (os.getcwd().endswith('tests')):
        return '.'
    else:
        return '.'


class TestTcp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SERVER = '%s/servers/tcp_upper_crlf.py' % servers_root()

        cls.process = subprocess.Popen(
            '%s %s' % (PY_COMMAND, SERVER),
            shell=True, preexec_fn=os.setsid
        )
        time.sleep(1.0)


    @classmethod
    def tearDownClass(cls):
       try:
            os.killpg(cls.process.pid, signal.SIGTERM)
       except:
           print("ERROR: Unable to kill PID %d" % cls.process.pid)


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
            sock.sendall("hello\r\nworld\r\n".encode('utf-8'))
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
        result =  sock.recv(len(data))
        result = result.decode('utf-8')
        self.assertEqual(data.upper(), result)

if __name__ == 'main':
    unittest.main()

