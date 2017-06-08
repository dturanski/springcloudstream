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

HOST, PORT = "localhost", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def random_data(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size)) + '\n'


def sendAndRecieve(data):
    sock.sendall(data)

    # Receive data from the server and shut down
    # Different for Python 3
    # str(sock.recv(1024),"utf-8")
    print("Sent:     {}".format(data).rstrip())
    received = str(sock.recv(len(data)))
    print("Received: {}".format(received))

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # sendAndRecieve('hello\n')
    sendAndRecieve(random_data(100))
    sendAndRecieve(random_data(1025))
    sendAndRecieve(random_data(2048))


finally:
    sock.close()

