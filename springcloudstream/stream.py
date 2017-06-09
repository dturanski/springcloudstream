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

import logging
import threading
import sys
import os
import os, sys
from optparse import OptionParser
import codecs

PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
    from socketserver import TCPServer
else:
    from SocketServer import TCPServer

from springcloudstream.tcp import StreamHandler, MonitorHandler

"""

"""


class Options:
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


class Processor:
    def __init__(self, handler_function, args=[]):
        self.handler_function = handler_function
        opts = Options(args)
        opts.validate()

        self.options = opts.options

        self.logger = logging.getLogger(__name__)


    def start(self):

        if not self.options.monitor_port:
            self.logger.warn(
                "Monitoring not enabled. No ping_port defined in initializer or 'PING_PORT' environment variable.")
        else:
            threading.Thread(target=self.monitor).start()

        # Create the server, binding to localhost on configured port
        self.logger.info('Starting server on port %d Python version %s.%s.%s' % ((self.options.port,) + sys.version_info[:3]))
        server = TCPServer(('localhost', self.options.port),
                           StreamHandler.create_handler(self.handler_function, self.options.encoder, self.options.buffer_size,
                                                        self.options.debug))

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

    def monitor(self):
        self.logger.info('Starting monitor server on port %d' % self.options.monitor_port)
        server = TCPServer(('localhost', self.options.monitor_port), MonitorHandler)
        server.serve_forever()
