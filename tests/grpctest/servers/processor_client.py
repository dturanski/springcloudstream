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

sys.path.append(os.path.abspath('./springcloudstream/grpc'))
sys.path.append(os.path.abspath('.'))
import grpc
from springcloudstream.proto.message_pb2 import Message
from springcloudstream.grpc.message import __convert_to_generic__

from springcloudstream.proto.processor_pb2_grpc import ProcessorStub
from springcloudstream.portability import long


def run():
    channel = grpc.insecure_channel('localhost:9999')
    stub = ProcessorStub(channel)
    for payload in [123, long(123), 123.4, True, "hello", bytes("hello")]:
        message = Message()
        __convert_to_generic__(message.payload, payload)
        message.headers['id'].string = '123'
        message.headers['timestamp'].long = 9999
        response = stub.Process(message)
        print("Processor client received: %s " % response)


if __name__ == '__main__':
    run()
