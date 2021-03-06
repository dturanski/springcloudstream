# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

from springcloudstream.proto import message_pb2 as message__pb2, processor_pb2 as processor__pb2


class ProcessorStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Ping = channel.unary_unary(
        '/processor.Processor/Ping',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=processor__pb2.Status.FromString,
        )
    self.Process = channel.unary_unary(
        '/processor.Processor/Process',
        request_serializer=message__pb2.Message.SerializeToString,
        response_deserializer=message__pb2.Message.FromString,
        )


class ProcessorServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Ping(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Process(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProcessorServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Ping': grpc.unary_unary_rpc_method_handler(
          servicer.Ping,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=processor__pb2.Status.SerializeToString,
      ),
      'Process': grpc.unary_unary_rpc_method_handler(
          servicer.Process,
          request_deserializer=message__pb2.Message.FromString,
          response_serializer=message__pb2.Message.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'processor.Processor', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
