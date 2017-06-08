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
__author__ = 'David Turanski'

import sys
import logging
import os
import threading


FORMAT = '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
logging.basicConfig(format=FORMAT, level=logging.ERROR)

# def binary_input(self):
#     buf = []
#     while True:
#         buf.append(binary_input.read(1))
#         if buf[-1] == '\x1a':
#             break
#
#     return ''.join(buf)
#
#
# if (data):
#     buffer.join(data)
# else:
#     done = True

PY3K = sys.version_info >= (3, 0)

if PY3K:
    import socketserver
else:
    import SocketServer


class Processor:
    def __init__(self, encoder=None, buffer_size=2048, debug=False, port=None, ping_port=None, **kwargs):
        self.encoder = encoder
        self.buffer_size = buffer_size
        self.debug = debug
        self.logger = logging.getLogger(__name__)

        self.port = os.environ.get('PORT', port)
        if not self.port:
            self.logger.error("No port defined in initializer or 'PORT' environment variable.")
            sys.exit(1)
        self.port = int(self.port)

        self.ping_port = os.environ.get('PING_PORT', ping_port)

        if self.ping_port:
            self.ping_port = int(self.ping_port)

    def start(self, handler_method):
        StreamHandler.create_handler(handler_method, self.encoder, self.buffer_size, self.debug)

        if not self.ping_port:
            self.logger.warn(
                "Monitoring not enabled. No ping_port defined in initializer or 'PING_PORT' environment variable.")
        else:
            threading.Thread(target=self.monitor).start()


            # Create the server, binding to localhost on configured port
        self.logger.info('Starting server on port %d' % self.port)
        server = SocketServer.TCPServer(('localhost', self.port),
                                        StreamHandler.create_handler(handler_method,
                                                                     self.encoder,
                                                                     self.buffer_size))

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

    def monitor(self):
        self.logger.info('Starting monitor server on port %d' % self.ping_port)
        server = SocketServer.TCPServer(('localhost', self.ping_port),MonitorHandler)
        server.serve_forever()


class StxEtxHandler(SocketServer.BaseRequestHandler):
    pass


class HeaderLengthHandler(SocketServer.BaseRequestHandler):
    @staticmethod
    def create_handler(handler_method, encoder=None, header_size=4, buffer_size=2048, debug=False):
        HeaderLengthHandler.BUFFER_SIZE = buffer_size
        HeaderLengthHandler.HEADER_SIZE = header_size
        HeaderLengthHandler.encoder = encoder
        HeaderLengthHandler.handler_method = staticmethod(handler_method)
        HeaderLengthHandler.logger = logging.getLogger(__name__)
        if (debug):
            HeaderLengthHandler.logger.setLevel(logging.DEBUG)
        return HeaderLengthHandler

    def handle(self):
        # self.request is the TCP socket connected to the client
        logger = HeaderLengthHandler.logger
        logger.debug("handling requests...")
        header =  bytearray(HeaderLengthHandler.HEADER_SIZE)
        buf = bytearray(HeaderLengthHandler.BUFFER_SIZE)
        received_data = bytearray()
        while True:
            logger.debug('waiting for more data')

            nbytes = self.request.recv_into(header, HeaderLengthHandler.HEADER_SIZE)
            if nbytes == 0:
                break

            data_size = int(header[:nbytes])
            remaining_bytes = data_size
            while remaining_bytes > 0:
                nbytes = self.request.recv_into(buf, min(data_size, HeaderLengthHandler.BUFFER_SIZE))

                if nbytes == 0:
                    break

                logger.debug("received %d bytes" % nbytes)
                logger.debug('[%s]' % buf[:nbytes])

                received_data.extend(buf[:nbytes])
                remaining_bytes = remaining_bytes - nbytes

            result = StreamHandler.handler_method(received_data)
            logger.debug("sending result [%s] to %s" % (result, self.client_address[0]))
            self.request.sendall(result)
            logger.debug("data sent")

        logger.warning("connection closed from %s" % (self.client_address[0]))
        self.request.close()


class StreamHandler(SocketServer.BaseRequestHandler):
    @staticmethod
    def create_handler(handler_method, encoder=None, buffer_size=2048, debug=False):
        StreamHandler.BUFFER_SIZE = buffer_size
        StreamHandler.encoder = encoder
        StreamHandler.handler_method = staticmethod(handler_method)
        StreamHandler.logger = logging.getLogger(__name__)
        if (debug):
            StreamHandler.logger.setLevel(logging.DEBUG)
        return StreamHandler

    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        logger = StreamHandler.logger
        logger.debug("handling requests...")
        buf = bytearray(StreamHandler.BUFFER_SIZE)

        received_data = bytearray()
        while True:
            logger.debug('waiting for more data')
            nbytes = self.request.recv_into(buf, StreamHandler.BUFFER_SIZE)

            if nbytes == 0:
                break

            logger.debug("received %d bytes" % nbytes)
            logger.debug('[%s]' % buf[:nbytes])

            received_data.extend(buf[:nbytes])

            terminator_pos = received_data.find('\n')
            logger.debug('terminator found @ [%d]' % terminator_pos)

            '''
            Handle multiple terminators in stream
            '''
            while terminator_pos != -1:
                data = received_data[:terminator_pos]
                logger.debug("received from %s: %s" % (self.client_address[0], data))
                # Do whatever you want with data here
                received_data = received_data[terminator_pos + 1:]
                # invoke the handler method on the data

                result = StreamHandler.handler_method(data)
                logger.debug("sending result [%s] to %s" % (result, self.client_address[0]))
                self.request.sendall(result)
                logger.debug("data sent")
                terminator_pos = received_data.find('\n')

        logger.warning("connection closed from %s" % (self.client_address[0]))
        self.request.close()


class MonitorHandler(SocketServer.BaseRequestHandler):

    def handle(self):
       logger = logging.getLogger(__name__)
       while True:
            data = self.request.recv(80)
            if not data:
                break

            logger.debug('got ping request %s' % data)
            self.request.sendall('alive\n');

       logger.warning("monitor connection closed from %s" % (self.client_address[0]))
       self.request.close()