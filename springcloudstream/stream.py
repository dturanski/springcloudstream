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

"""

"""


import logging
import threading
import sys
import os
import os, sys
from optparse import OptionParser
import codecs

from springcloudstream.tcp import launch_server
from springcloudstream.messagehandler import *

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

    @classmethod
    def value(cls, name):
        return cls.__dict__[name]

class Options:
    """
    Encapsulates on OptionParser to handle options for BaseStreamComponent
    """
    def __init__(self, args):
        self.parser = OptionParser()

        self.parser.usage = "%prog [options] --help for help"

        self.parser.add_option('-p', '--port',
                               type='int',
                               help='the socket port to use',
                               dest='port')
        self.parser.add_option('-m', '--monitor-port',
                               type='int',
                               help='the socket to use for the monitoring server',
                               dest='monitor_port')

        self.parser.add_option('-s', '--buffer-size',
                               help='the tcp buffer size',
                               default=2048,
                               dest='buffer_size')

        self.parser.add_option('-d', '--debug',
                               action='store_true',
                               help='turn on debug logging',
                               default=False,
                               dest='debug')

        self.parser.add_option('-c', '--char-encoding',
                               help='character encoding',
                               default='utf-8',
                               dest='char_encoding')

        self.parser.add_option('-e', '--encoder',
                               type="choice",
                               choices=['CR', 'CRLF', 'STXETX', 'L4', 'L2', 'L1'],
                               help='The name of the encoder to use for delimiting messages',
                               default='CR',
                               dest='encoder')

        self.options, arguments = self.parser.parse_args(args)

    def validate(self):
        """
        Validate the options or exit()
        """
        if not self.options.port:
            print("'port' is required")
            sys.exit(2)
        if self.options.port == self.options.monitor_port:
            print("'port' and 'monitor-port' must not be the same.")
            sys.exit(2)
        if self.options.buffer_size <= 0:
            print("'buffer_size' must be > 0.")
            sys.exit(2)
        try:
            codecs.getencoder(self.options.char_encoding)
        except LookupError:
            print("invalid 'char-encoding' %s" % self.options.char_encoding)
            sys.exit(2)


class BaseStreamComponent:
    """
    The Base class for Stream Components
    """
    def __init__(self, handler_function, args=[]):
        """
        :param handler_function: The function to execute on each message
        :param args: command line options or list representing as sys.argv
        """

        opts = Options(args)
        opts.validate()
        self.options = opts.options
        self.message_handler = self.create_message_handler(handler_function)

    def start(self):
        """
        Start the server and run forever.
        """
        launch_server(self.message_handler, self.options)

    def create_message_handler(self,handler_function):
        """
        Create a MessageHandler for the configured Encoder
        :param handler_function: The function to execute on each message
        :return: a MessageHandler
        """
        encoder = Encoders.value(self.options.encoder)
        if encoder == None or encoder == Encoders.CR:
            return DefaultMessageHandler(handler_function)
        elif encoder == Encoders.STXETX:
            return StxEtxHandler(handler_function)
        elif encoder == Encoders.CRLF:
            return CrlfHandler(handler_function)
        elif encoder == Encoders.L4:
            return HeaderLengthHandler(4, handler_function)
        elif encoder == Encoders.L2:
            return HeaderLengthHandler(2, handler_function)
        elif encoder == Encoders.L1:
            return HeaderLengthHandler(1, handler_function)
        else:
            raise NotImplementedError('No RequestHandler defined for given encoder (%s).' % self.options.encoder)



class Processor(BaseStreamComponent):
    """Stream Processor - receives and sends messages."""

    def __init__(self, handler_function, args=[]):
        BaseStreamComponent.__init__(self, handler_function, args)


class Sink(BaseStreamComponent):
    """Stream Sink - receives messages only"""

    def __init__(self, handler_function, args=[]):
        BaseStreamComponent.__init__(self, handler_function, args)


class Source(BaseStreamComponent):
    """Stream Source - sends messages from an external pollable or event driven source """

    def __init__(self, handler_function, args=[]):
        BaseStreamComponent.__init__(self, handler_function, args)
