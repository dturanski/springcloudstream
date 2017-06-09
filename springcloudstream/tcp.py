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
__author__ = 'David Turanski'

__version__ = '1.0.1'

"""
This module supports the use TCP sockets for communication between local processes.  
"""

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
    from socketserver import BaseRequestHandler
else:
    from SocketServer import BaseRequestHandler


class Encoders:
    """Named identifiers to determine which RequestHandler to use.
       CRLF - messages are terminated by '\r\n'
       CR - The default - messages are terminated by '\n'
       L4 - Messages include a 4 byte header containing the length of the message (max length = 2**31 - 1)
       L2 - Messages include a 2 byte unsigned short header containing the length of the message (max length = 2**16)
       L1 - Messages include a 1 byte header containing the length of the message (max length = 255)
       STXETX - Messages begin with stx '0x2' and end with etx '0x3'
    """
    CRLF, CR, STXETX, L4, L2, L1 = range(6)


class MessageHandler:
    """
    Base Message Handler.
    Called by StreamHandler to encode/decode socket message and invoke the handler_function.
    """
    def __init__(self, handler_function):
        self.handler_function = handler_function


class DefaultMessageHandler(MessageHandler):
    """
    Default Message Handler for str terminated by CR ('\n')
    """
    def handle(self, request, received_data, buf, logger):
        """
        Handles a socket message.

        :param request: the request socket
        :param received_data: accumulated data across multiple socket recvs
        :param buf: the data for each socket recv invocation.
        :param logger: the logger to use.
        :return: updated received_data or None if the socket connection was terminated.
        """
        try:
            nbytes = request.recv_into(buf, len(buf))
        except:
            return None

        if nbytes > 0:

            logger.debug("received %d bytes" % nbytes)
            received_data.extend(buf[:nbytes])

            terminator_pos = received_data.find(b'\n')
            logger.debug('terminator found @ [%d]' % terminator_pos)

            '''
            Handle multiple occurences of terminators in stream
            '''
            while terminator_pos != -1:
                data = received_data[:terminator_pos].decode('utf-8')
                logger.debug("received [%s]" % data )
                received_data = received_data[terminator_pos + 1:]
                # invoke the handler function on the data
                result = self.handler_function(data)
                logger.debug("sending result [%s]" % result)

                if result.find('\n') != len(result) - 1:
                    result = result + '\n'
                try:
                    request.sendall(result.encode('utf-8'))
                    logger.debug("data sent")
                except :
                    logger.error("data not sent %s" % sys.exc_info()[0])
                    return None

                terminator_pos = received_data.find(b'\n')
            return received_data
        else:
            return None



class StxEtxHandler(MessageHandler):
    """"""
    pass


class CrlfHandler(MessageHandler):
    """"""
    pass



class HeaderLengthHandler(MessageHandler):
    """
    A RequestHandler that encodes/decodes using a message length header.
    """
    LONG = '!L'
    SHORT = '!H'
    BYTE = 'B'
    FORMATS = {4: LONG, 2: SHORT, 1: BYTE}

    def __init__(self, header_size, handler_function):
        MessageHandler.__init__(self, handler_function)
        if not header_size in (1, 2, 4):
            raise RuntimeError('Invalid header_size. Valid values are 1, 2 and 4')
        self.HEADER_SIZE = header_size
        self.FORMAT = HeaderLengthHandler.FORMATS[header_size]

    def handle(self, request, received_data, buf ,logger):
        header = bytearray(self.HEADER_SIZE)
        try:
            nbytes = request.recv_into(header, self.HEADER_SIZE)
        except:
            return None

        if nbytes > 0:
            data_size = self.__data_size(header)
            logger.debug("data size is %d bytes" % data_size)
            remaining_bytes = data_size
            while remaining_bytes > 0:
                try:
                    nbytes = request.recv_into(buf, min(data_size, len(buf)))
                except:
                    return None

                if nbytes == 0:
                    return None

                logger.debug("received %d bytes" % nbytes)
                logger.debug('received [%s]' % buf[:nbytes])

                received_data.extend(buf[:nbytes])
                remaining_bytes = remaining_bytes - nbytes

            result = self.handler_function(received_data)
            logger.debug("sending result [%s]" % result)

            try:
                request.sendall(self.__encode(result))
                logger.debug("data sent")
            except:
                logger.error("data not sent %s" % sys.exc_info())
                return None

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



class StreamHandler(BaseRequestHandler):
    """
    A RequestHandler that waits for messages over its request socket until the socket is closed
     and delegates to a MessageHandler
    """
    @classmethod
    def create_handler(cls, handler_function, encoder=Encoders.CR, buffer_size=2048, debug=False):
        cls.BUFFER_SIZE = buffer_size
        ''' Declared as static to avoid requirement for implicit class argument.'''
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
            received_data = request_handler.handle(self.request, received_data, buf, logger)
            if received_data == None:
                break

        logger.warning("connection closed from %s" % (self.client_address[0]))
        self.request.close()

    def create_request_handler(self):
        encoder = StreamHandler.encoder
        handler_function = StreamHandler.handler_function
        if encoder == None or encoder == Encoders.CR:
            return DefaultMessageHandler(handler_function)
        elif self.encoder == Encoders.STXETX:
            return StxEtxHandler(handler_function)
        elif self.encoder == Encoders.CRLF:
            return CrlfHandler(handler_function)
        elif self.encoder == Encoders.L4:
            return HeaderLengthHandler(4, handler_function)
        elif self.encoder == Encoders.L2:
            return HeaderLengthHandler(2, handler_function)
        elif self.encoder == Encoders.L1:
            return HeaderLengthHandler(1, handler_function)
        else:
            raise NotImplementedError('No RequestHandler defined for given encoder.')


class MonitorHandler(BaseRequestHandler):
    """Starts a monitor server to allow external processes to check the status"""
    def handle(self):
        logger = logging.getLogger(__name__)
        while True:
            data = self.request.recv(80)
            if not data:
                break

            logger.debug('got ping request %s' % data)
            self.request.sendall('alive\n'.encode('utf-8'));

        logger.warning("monitor connection closed  %s" % (self.client_address[0]))
        self.request.close()
