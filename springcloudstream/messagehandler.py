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

__version__ = '1.0.1'

"""
Implementations of MessageHandler used by stream components.
"""

import struct
import sys


class MessageHandler:
    """
    Base Message Handler.
    Called by StreamHandler to encode/decode socket message and invoke the handler_function.
    """

    def __init__(self, handler_function, component_type, char_encoding='utf-8'):
        """
        :param handler_function: the handler function to execute for each message.
        """
        self.handler_function = handler_function
        self.char_encoding = char_encoding
        if not component_type in ('Processor', 'Sink'):
            raise NotImplementedError("component type %s is not implemented" % component_type)

        self.component_type = component_type




class DefaultMessageHandler(MessageHandler):
    """
    Default Message Handler for str terminated by CR ('\n')
    """

    def __init__(self, handler_function, component_type, char_encoding='utf-8'):


    def __receive(self, request, buffer_size):
        logger = self.logger
        buf = bytearray(buffer_size)
        received_data = bytearray()
        receive_complete = False
        data = None
        try:
            while not receive_complete:
                nbytes = request.recv_into(buf, buffer_size)
                if nbytes > 0:
                    logger.debug("received %d bytes " % nbytes)
                    received_data.extend(buf[:nbytes])
                    receive_complete = (received_data.rfind(b'\n') == len(received_data) - 1)

                    if receive_complete:
                        data = received_data.decode(self.char_encoding)
                        logger.debug('message received [%s]' % data)
                else:
                    break

        except Exception:
            logger.error("Error receiving message %s ", sys.exc_info())

        return data

    def __send(self, request, msg):
        logger = self.logger

        logger.debug("sending result [%s]" % msg)

        if msg.find('\n') != len(msg) - 1:
            msg += '\n'
        try:
            request.sendall(msg.encode(self.char_encoding))
            logger.debug("data sent")
        except:
            logger.error("data not sent %s" % sys.exc_info()[0])
            return False
        return True

    def handle(self, request, buffer_size):
        """
        Handle a message
        :param request: the request socket.
        :param buffer_size: the buffer size.
        :return: True if success, False otherwise
        """
        logger = self.logger

        data = self.__receive(request, buffer_size)
        if data is None:
            return False
        else:
            for message in data.split('\n')[:-1]:
                result = self.handler_function(message)
                if self.component_type == 'Processor':
                    if not self.__send(request, result):
                        return False
        return True


class StxEtxHandler(MessageHandler):
    """"""
    pass


class CrlfHandler(MessageHandler):
    """
    Message Handler for str terminated by CRLF ('\r\n')
    """

    def __receive(self, request, buffer_size):
        logger = self.logger
        buf = bytearray(buffer_size)
        received_data = bytearray()
        receive_complete = False
        data = None
        try:
            while not receive_complete:
                nbytes = request.recv_into(buf, buffer_size)
                if nbytes > 0:
                    logger.debug("received %d bytes " % nbytes)
                    received_data.extend(buf[:nbytes])
                    receive_complete = \
                        (received_data.rfind(b'\n') == len(received_data) - 1) and \
                        (received_data.rfind(b'\r') == len(received_data) - 2)

                    if receive_complete:
                        data = received_data.decode(self.char_encoding)
                        logger.debug('message received [%s]' % data)
                else:
                    break

        except Exception:
            logger.error("Error receiving message %s ", sys.exc_info())

        return data

    def __send(self, request, msg):
        logger = self.logger
        logger.debug("sending result [%s]" % msg)
        if msg.find('\r\n') != len(msg) - 2:
            msg += '\r\n'
        try:
            request.sendall(msg.encode(self.char_encoding))
            logger.debug("data sent")

        except:
            logger.error("data not sent %s" % sys.exc_info()[0])
            return False

        return True

    def handle(self, request, buffer_size):
        """
        Handle a message
        :param request: the request socket.
        :param buffer_size: the buffer size.
        :return: True if success, False otherwise
        """
        logger = self.logger

        data = self.__receive(request, buffer_size)
        if data is None:
            return False
        else:
            for message in data.split('\r\n')[:-1]:
                result = self.handler_function(message)
                if self.component_type == 'Processor':
                    if not self.__send(request, result):
                        return False
        return True


class HeaderLengthHandler(MessageHandler):
    """
    A RequestHandler that encodes/decodes using a message length header.
    """
    LONG = '!L'
    SHORT = '!H'
    BYTE = 'B'
    FORMATS = {4: LONG, 2: SHORT, 1: BYTE}

    def __init__(self, header_size, handler_function, component_type):
        """
        :param header_size: the size of the message length header in bytes (1,2, or 4)
        :param handler_function: the handler function to execute for each message
        """
        MessageHandler.__init__(self, handler_function, component_type)
        if not header_size in (1, 2, 4):
            raise RuntimeError('Invalid header_size. Valid values are 1, 2 and 4')
        self.HEADER_SIZE = header_size
        self.FORMAT = HeaderLengthHandler.FORMATS[header_size]

    def __receive(self, request, buffer_size):
        logger = self.logger
        buf = bytearray(buffer_size)
        header = bytearray(self.HEADER_SIZE)
        received_data = bytearray()
        receive_complete = False
        data = None
        try:
            while not receive_complete:
                nbytes = request.recv_into(header, self.HEADER_SIZE)
                if nbytes > 0:
                    data_size = self.__data_size(header)
                    remaining_bytes = data_size
                    while remaining_bytes > 0:
                        nbytes = request.recv_into(buf, min(data_size, buffer_size))
                        if nbytes > 0:
                            logger.debug("received %d bytes " % nbytes)
                            received_data.extend(buf[:nbytes])
                            remaining_bytes -= nbytes

                    receive_complete = True
                    data = received_data.decode(self.char_encoding)
                    logger.debug('message received [%s]' % data)
                else:
                    break

        except Exception:
            logger.error("Error receiving message %s ", sys.exc_info())

        return data

    def __send(self, request, msg):
        logger = self.logger
        logger.debug("sending result [%s]" % msg)

        try:
            request.sendall(self.__encode(msg))
            logger.debug("data sent")
        except:
            logger.error("data not sent %s" % sys.exc_info())
            return False

        return True

    def handle(self, request, buffer_size):
        """
        Handle a message
        :param request: the request socket.
        :param buffer_size: the buffer size.
        :return: True if success, False otherwise
        """
        logger = self.logger
        msg = self.__receive(request, buffer_size)
        if msg is None:
            return False

        result = self.handler_function(msg)

        if self.component_type == 'Processor':
            return self.__send(request, result)
        return True

    def __encode(self, data):
        ba = bytearray(struct.pack(self.FORMAT, len(data)))
        ba.extend(bytearray(data, self.char_encoding))
        return ba

    def __data_size(self, header):
        data_size = struct.unpack(self.FORMAT, header)[0]
        if self.FORMAT == HeaderLengthHandler.BYTE:
            data_size = ord(header)
        return data_size
