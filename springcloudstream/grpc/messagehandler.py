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

__version__ = '1.1.0'

"""
Implementations of MessageHandler used by stream components.
"""
import sys
import time
import logging
from springcloudstream.grpc.stream_component import StreamComponent
from springcloudstream.grpc.message import Message, MessageHeaders
import springcloudstream.grpc.processor_pb2 as processor_pb2
import springcloudstream.grpc.processor_pb2_grpc as processor_pb2_grpc
import grpc
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
    long = int
    from inspect import getfullargspec
else:
    from inspect import getargspec as getfullargspec


FORMAT = '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


class MessageHandler(processor_pb2_grpc.ProcessorServicer):
    """
    Message Handler for Grpc
    """

    def __init__(self, handler_function, component_type):
        """
         Translate the Protobuf Message and invoke the handler_function.
        :param handler_function: the handler function to execute for each message.
        """
        self.handler_function = handler_function
        if not component_type in StreamComponent.components:
            raise NotImplementedError("component type %s is not implemented" % component_type)

        self.component_type = component_type


    def Ping(self, request, context):
        # missing associated documentation comment in .proto file
        pass
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Process(self, request, context):
        """
        Invoke the Grpc Processor, delegating to the handler_function. If the handler_function has a single argument,
        pass the Message payload. If two arguments, pass the payload and headers as positional arguments:
        handler_function(payload, headers). If the handler function return is not of type(Message), create a new Message using
        the original header values (new id and timestamp).

        :param request: the message
        :param context: the request context
        :return: response message
        """
        logger.debug(request)
        logger.debug('payload type: %s' % type(request.payload.string))
        message = Message.__from_protobuf_message__(request)
        sig = getfullargspec(self.handler_function)
        if len(sig.args) == 2:
            result = self.handler_function(message.payload, message.headers)
        elif len(sig.args) == 1:
            result = self.handler_function(message.payload)
        else:
            raise RuntimeError('wrong number of arguments for handler function - must be 1 or 2')

        if self.component_type == StreamComponent.PROCESSOR:
            if type(result) == Message:
                return result.__to_protobuf_message__()
            else:
                headers = MessageHeaders()
                headers.copy(message.headers)
                return Message(result, headers).__to_protobuf_message__()




logger = logging.getLogger(__name__)

class Server:

    def start(self, options, handler_function, component_type):

        if options.debug:
            logger.setLevel(logging.DEBUG)

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=options.thread_pool_size),maximum_concurrent_rpcs=options.max_concurrent_rpcs)
        processor_pb2.add_ProcessorServicer_to_server(MessageHandler(handler_function,component_type), server)
        server.add_insecure_port('[::]:%d' % options.port)
        server.start()
        logger.info("server started %s" % options)

        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)