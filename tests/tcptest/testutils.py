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
import os
import unittest
import subprocess
import signal
import time

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

HOST, PORT = socket.gethostname(), 9999

PYTHON3 = sys.version_info >= (3, 0)

PY_COMMAND = 'python'
if PYTHON3:
    PY_COMMAND = 'python3'


class TcpTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SERVER = '%s/%s' % (cls.servers_root(), cls.SERVER_NAME)

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

    @classmethod
    def servers_root(cls):
        if os.getcwd().endswith('springcloudstream'):
            return '%s/tests/tcptest/servers' % os.getcwd()
        elif os.getcwd().endswith('tcptest'):
            return '%s/servers' % os.getcwd()
        elif os.getcwd().endswith("tests"):
            return '%s/tcptest/servers' % os.getcwd()

    def create_socket(self, port=PORT):
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, port))
        return sock
