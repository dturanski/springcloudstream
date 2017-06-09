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
                data = received_data[:terminator_pos].decode(self.char_encoding)
                logger.debug("received [%s]" % data)
                received_data = received_data[terminator_pos + 1:]

                # invoke the handler function on the data
                result = self.handler_function(data)

                if self.component_type == 'Processor':
                    logger.debug("sending result [%s]" % result)

                    if result.find('\n') != len(result) - 1:
                        result = result + '\n'
                    try:
                        request.sendall(result.encode(self.char_encoding))
                        logger.debug("data sent")
                    except:
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

    def handle(self, request, received_data, buf, logger):
        """
        Handles a socket message.

        :param request: the request socket
        :param received_data: accumulated data across multiple socket recvs
        :param buf: the data for each socket recv invocation.
        :param logger: the logger to use.
        :return: updated received_data or None if the socket connection was terminated.
        """
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

            if self.component_type == 'Processor':
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
