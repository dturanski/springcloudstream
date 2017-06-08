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
import struct
from abc import abstractmethod, ABCMeta

FORMAT = '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
    from socketserver import BaseRequestHandler, TCPServer
else:
    from SocketServer import BaseRequestHandler, TCPServer


class Encoders:
    CRLF, LF, STXETX, L4, L2, L1 = range(6)


"""
"""


class Processor:
    def __init__(self, encoder=None, buffer_size=2048, debug=False, port=None, ping_port=None):
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

    def start(self, handler_function):

        if not self.ping_port:
            self.logger.warn(
                "Monitoring not enabled. No ping_port defined in initializer or 'PING_PORT' environment variable.")
        else:
            threading.Thread(target=self.monitor).start()

        # Create the server, binding to localhost on configured port
        self.logger.info('Starting server on port %d Python version %s.%s.%s' % ( (self.port,) + sys.version_info[:3]) )
        server = TCPServer(('localhost', self.port),
                                        StreamHandler.create_handler(handler_function, self.encoder, self.buffer_size,
                                                                     self.debug))

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

    def monitor(self):
        self.logger.info('Starting monitor server on port %d' % self.ping_port)
        server = TCPServer(('localhost', self.ping_port), MonitorHandler)
        server.serve_forever()





class RequestHandler:
    """
    Base Request Handler.

    Called by StreamHandler to encode/decode data and invoke the handler_function.
    """
    def __init__(self, handler_function, request, logger, client_address):
        self.handler_function = handler_function
        self.request = request
        self.logger = logger
        self.client_address = client_address


class DefaultRequestHandler(RequestHandler):
    """
    Default Socket Handler for str terminated by LF ('\n'). Return None to close the connection.
    """
    def handle(self, received_data, buf):
        try:
            nbytes = self.request.recv_into(buf, len(buf))
        except:
            return None

        if nbytes > 0:

            self.logger.debug("received %d bytes" % nbytes)
            received_data.extend(buf[:nbytes])

            terminator_pos = received_data.find(b'\n')
            self.logger.debug('terminator found @ [%d]' % terminator_pos)

            '''
            Handle multiple occurences of terminators in stream
            '''
            while terminator_pos != -1:
                data = received_data[:terminator_pos].decode('utf-8')
                self.logger.debug("received from %s: %s" % (self.client_address, data))
                received_data = received_data[terminator_pos + 1:]
                # invoke the handler function on the data
                result = self.handler_function(data)
                self.logger.debug("sending result [%s] to %s" % (result, self.client_address))

                if result.find('\n') != len(result) - 1:
                    result = result + '\n'
                try:
                    self.request.sendall(result.encode('utf-8'))
                    self.logger.debug("data sent")
                except :
                    self.logger.warn("data not sent %s" % sys.exc_info()[0])
                    return None

                terminator_pos = received_data.find(b'\n')
            return received_data
        else:
            return None


"""
"""


class StxEtxHandler(RequestHandler):
    pass


"""
"""


class CrlfHandler(RequestHandler):
    pass




class HeaderLengthHandler(RequestHandler):
    """
    A RequestHandler that encodes/decodes using a message length header.
    """
    LONG = '!L'
    SHORT = '!H'
    BYTE = 'B'
    FORMATS = {4: LONG, 2: SHORT, 1: BYTE}

    def __init__(self, header_size, handler_function, request, logger, client_address):
        RequestHandler.__init__(self, handler_function, request, logger, client_address)
        if not header_size in (1, 2, 4):
            raise RuntimeError('Invalid header_size. Valid values are 1, 2 and 4')
        self.HEADER_SIZE = header_size
        self.FORMAT = HeaderLengthHandler.FORMATS[header_size]

    def handle(self, received_data, buf):
        logger = self.logger
        header = bytearray(self.HEADER_SIZE)
        try:
            nbytes = self.request.recv_into(header, self.HEADER_SIZE)
        except:
            return None

        if nbytes > 0:
            data_size = self.__data_size(header)
            logger.debug("data size is %d bytes" % data_size)
            remaining_bytes = data_size
            while remaining_bytes > 0:
                try:
                    nbytes = self.request.recv_into(buf, min(data_size, len(buf)))
                except:
                    return None

                if nbytes == 0:
                    return None

                logger.debug("received %d bytes" % nbytes)
                logger.debug('[%s]' % buf[:nbytes])

                received_data.extend(buf[:nbytes])
                remaining_bytes = remaining_bytes - nbytes

            result = self.handler_function(received_data)
            logger.debug("sending result [%s] to %s" % (result, self.client_address))
            self.request.sendall(self.__encode(result))
            logger.debug("data sent")
            received_data = bytearray()
            return received_data
        else:
            return None

    def __encode(self, data):
        ba = bytearray(struct.pack(self.FORMAT, len(data)))
        ba.extend(data)
        return ba

    def __data_size(self, header):
        data_size = struct.unpack(self.FORMAT, header)[0]
        if self.FORMAT == HeaderLengthHandler.BYTE:
            data_size = ord(header)
        return data_size


"""
"""


class StreamHandler(BaseRequestHandler):
    @classmethod
    def create_handler(cls, handler_function, encoder=Encoders.LF, buffer_size=2048, debug=False):
        cls.BUFFER_SIZE = buffer_size
        cls.handler_function = staticmethod(handler_function)
        cls.encoder = encoder
        cls.logger = logging.getLogger(__name__)
        if (debug):
            cls.logger.setLevel(logging.DEBUG)
        return cls

    """
       The request handler class for the server.
       It is instantiated once per connection to the server, and must
       override the handle() method to implement communication to the
       client.
    """

    def handle(self):
        logger = StreamHandler.logger
        logger.debug("handling requests...")

        request_handler = self.create_request_handler()
        received_data = bytearray()

        while True:
            logger.debug('waiting for more data')
            buf = bytearray(StreamHandler.BUFFER_SIZE)
            received_data = request_handler.handle(received_data, buf)
            if received_data == None:
                break

        logger.warning("connection closed from %s" % (self.client_address[0]))
        self.request.close()

    def create_request_handler(self):
        encoder = StreamHandler.encoder
        handler_function = StreamHandler.handler_function
        if encoder == None or encoder == Encoders.LF:
            return DefaultRequestHandler(handler_function, self.request, StreamHandler.logger, self.client_address[0])
        elif self.encoder == Encoders.STXETX:
            return StxEtxHandler(handler_function, self.request, StreamHandler.logger, self.client_address[0])
        elif self.encoder == Encoders.CRLF:
            return CrlfHandler(handler_function, self.request, StreamHandler.logger, self.client_address[0])
        elif self.encoder == Encoders.L4:
            return HeaderLengthHandler(4, handler_function, self.request, StreamHandler.logger, self.client_address[0])
        elif self.encoder == Encoders.L2:
            return HeaderLengthHandler(2, handler_function, self.request, StreamHandler.logger, self.client_address[0])
        elif self.encoder == Encoders.L1:
            return HeaderLengthHandler(1, handler_function, self.request, StreamHandler.logger, self.client_address[0])
        else:
            raise NotImplementedError('No RequestHandler defined for given encoder.')


class MonitorHandler(BaseRequestHandler):
    def handle(self):
        logger = logging.getLogger(__name__)
        while True:
            data = self.request.recv(80)
            if not data:
                break

            logger.debug('got ping request %s' % data)
            self.request.sendall('alive\n'.encode('utf-8'));

        logger.warning("monitor connection closed from %s" % (self.client_address[0]))
        self.request.close()
