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

import os
import sys
import subprocess
import signal
import time
import unittest

import grpc
from google.protobuf.empty_pb2 import Empty
from springcloudstream.proto.message_pb2 import Message
from springcloudstream.proto.processor_pb2_grpc import ProcessorStub

PORT = 9999
SCRIPT = 'upper_grpc.py'

PYTHON3 = sys.version_info >= (3, 0)

PY_COMMAND = 'python'
if PYTHON3:
    PY_COMMAND = 'python3'


def servers_root():
    if os.getcwd().endswith('springcloudstream'):
        return '%s/tests/servers' % os.getcwd()
    elif os.getcwd().endswith('grpc'):
        return '%s/../servers' % os.getcwd()
    else:
        return '.'


class GrpcServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SERVER = '%s/%s' % (servers_root(),SCRIPT)
        command = "%s %s --port=%d --debug" % (PY_COMMAND,SERVER,PORT)
        cls.process = subprocess.Popen(command,
            shell=True, preexec_fn=os.setsid
        )
        time.sleep(2.0)

        channel = grpc.insecure_channel('localhost:%d' % PORT)
        cls.processor = ProcessorStub(channel)

    @classmethod
    def tearDownClass(cls):
        try:
            os.killpg(cls.process.pid, signal.SIGTERM)
        except:
            print("ERROR: Unable to kill PID %d" % cls.process.pid)

    def test_messsage(self):
        request = Message()
        request.payload.string="hello"
        response = self.processor.Process(request)
        self.assertEqual('HELLO',response.payload.string)

    def test_ping(self):
        response = self.processor.Ping(Empty())
        self.assertEqual('alive',response.message)

