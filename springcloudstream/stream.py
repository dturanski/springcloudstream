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



PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
    from socketserver import TCPServer
else:
    from SocketServer import TCPServer

from springcloudstream.tcp import StreamHandler, MonitorHandler

"""

"""

class Processor:
    def __init__(self, handler_function, encoder=None, buffer_size=2048, debug=False, port=None, ping_port=None):
        self.handler_function = handler_function
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

    def start(self):

        if not self.ping_port:
            self.logger.warn(
                "Monitoring not enabled. No ping_port defined in initializer or 'PING_PORT' environment variable.")
        else:
            threading.Thread(target=self.monitor).start()

        # Create the server, binding to localhost on configured port
        self.logger.info('Starting server on port %d Python version %s.%s.%s' % ( (self.port,) + sys.version_info[:3]) )
        server = TCPServer(('localhost', self.port),
                                        StreamHandler.create_handler(self.handler_function, self.encoder, self.buffer_size,
                                                                     self.debug))

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

    def monitor(self):
        self.logger.info('Starting monitor server on port %d' % self.ping_port)
        server = TCPServer(('localhost', self.ping_port), MonitorHandler)
        server.serve_forever()
