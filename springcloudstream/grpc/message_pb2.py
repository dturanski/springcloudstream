# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='message',
  syntax='proto3',
  serialized_pb=_b('\n\rmessage.proto\x12\x07message\"\x9e\x01\n\x07Message\x12!\n\x07payload\x18\x14 \x01(\x0b\x32\x10.message.Generic\x12.\n\x07headers\x18\x15 \x03(\x0b\x32\x1d.message.Message.HeadersEntry\x1a@\n\x0cHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1f\n\x05value\x18\x02 \x01(\x0b\x32\x10.message.Generic:\x02\x38\x01\"\x86\x01\n\x07Generic\x12\x10\n\x06string\x18\x01 \x01(\tH\x00\x12\x0f\n\x05\x62ytes\x18\x02 \x01(\x0cH\x00\x12\x0e\n\x04long\x18\x03 \x01(\x03H\x00\x12\r\n\x03int\x18\x04 \x01(\x05H\x00\x12\x0e\n\x04\x62ool\x18\x05 \x01(\x08H\x00\x12\x10\n\x06\x64ouble\x18\x06 \x01(\x01H\x00\x12\x0f\n\x05\x66loat\x18\x07 \x01(\x02H\x00\x42\x06\n\x04typeBD\n1org.springframework.cloud.stream.app.grpc.messageB\rMessageProtosP\x01\x62\x06proto3')
)




_MESSAGE_HEADERSENTRY = _descriptor.Descriptor(
  name='HeadersEntry',
  full_name='message.Message.HeadersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='message.Message.HeadersEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='message.Message.HeadersEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=121,
  serialized_end=185,
)

_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='message.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payload', full_name='message.Message.payload', index=0,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='headers', full_name='message.Message.headers', index=1,
      number=21, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_MESSAGE_HEADERSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=185,
)


_GENERIC = _descriptor.Descriptor(
  name='Generic',
  full_name='message.Generic',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='string', full_name='message.Generic.string', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bytes', full_name='message.Generic.bytes', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='long', full_name='message.Generic.long', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='int', full_name='message.Generic.int', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bool', full_name='message.Generic.bool', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='double', full_name='message.Generic.double', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='float', full_name='message.Generic.float', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='type', full_name='message.Generic.type',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=188,
  serialized_end=322,
)

_MESSAGE_HEADERSENTRY.fields_by_name['value'].message_type = _GENERIC
_MESSAGE_HEADERSENTRY.containing_type = _MESSAGE
_MESSAGE.fields_by_name['payload'].message_type = _GENERIC
_MESSAGE.fields_by_name['headers'].message_type = _MESSAGE_HEADERSENTRY
_GENERIC.oneofs_by_name['type'].fields.append(
  _GENERIC.fields_by_name['string'])
_GENERIC.fields_by_name['string'].containing_oneof = _GENERIC.oneofs_by_name['type']
_GENERIC.oneofs_by_name['type'].fields.append(
  _GENERIC.fields_by_name['bytes'])
_GENERIC.fields_by_name['bytes'].containing_oneof = _GENERIC.oneofs_by_name['type']
_GENERIC.oneofs_by_name['type'].fields.append(
  _GENERIC.fields_by_name['long'])
_GENERIC.fields_by_name['long'].containing_oneof = _GENERIC.oneofs_by_name['type']
_GENERIC.oneofs_by_name['type'].fields.append(
  _GENERIC.fields_by_name['int'])
_GENERIC.fields_by_name['int'].containing_oneof = _GENERIC.oneofs_by_name['type']
_GENERIC.oneofs_by_name['type'].fields.append(
  _GENERIC.fields_by_name['bool'])
_GENERIC.fields_by_name['bool'].containing_oneof = _GENERIC.oneofs_by_name['type']
_GENERIC.oneofs_by_name['type'].fields.append(
  _GENERIC.fields_by_name['double'])
_GENERIC.fields_by_name['double'].containing_oneof = _GENERIC.oneofs_by_name['type']
_GENERIC.oneofs_by_name['type'].fields.append(
  _GENERIC.fields_by_name['float'])
_GENERIC.fields_by_name['float'].containing_oneof = _GENERIC.oneofs_by_name['type']
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
DESCRIPTOR.message_types_by_name['Generic'] = _GENERIC
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(

  HeadersEntry = _reflection.GeneratedProtocolMessageType('HeadersEntry', (_message.Message,), dict(
    DESCRIPTOR = _MESSAGE_HEADERSENTRY,
    __module__ = 'message_pb2'
    # @@protoc_insertion_point(class_scope:message.Message.HeadersEntry)
    ))
  ,
  DESCRIPTOR = _MESSAGE,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:message.Message)
  ))
_sym_db.RegisterMessage(Message)
_sym_db.RegisterMessage(Message.HeadersEntry)

Generic = _reflection.GeneratedProtocolMessageType('Generic', (_message.Message,), dict(
  DESCRIPTOR = _GENERIC,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:message.Generic)
  ))
_sym_db.RegisterMessage(Generic)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n1org.springframework.cloud.stream.app.grpc.messageB\rMessageProtosP\001'))
_MESSAGE_HEADERSENTRY.has_options = True
_MESSAGE_HEADERSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)