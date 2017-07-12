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
Provide support for using grpc with Spring Cloud Stream
"""

import message_pb2
import uuid
import time
import collections


class MessageHeaders(collections.MutableMapping):
    """
     dict like object to enforce Spring MessageHeaders compatibility.
    """
    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)
        self.__dict__['id'] = str(uuid.uuid4())
        self.__dict__['timestamp'] = int(round(time.time() * 1000))


    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        if key == 'id' or key == 'timestamp':
            raise KeyError("key '%s' cannot be updated" % key)
        __check_supported_type__(value)
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        if key == 'id' or key == 'timestamp':
            raise KeyError("key '%s' cannot be deleted" % key)
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    # The final two methods aren't required, but nice for demo purposes:
    def __str__(self):
        '''returns simple dict representation of the mapping'''
        return str(self.__dict__)

    def __repr__(self):
        '''echoes class, id, & reproducible representation in the REPL'''
        return '{}, MessageHeaders({})'.format(super(MessageHeaders, self).__repr__(),
                                               self.__dict__)


class Message:
    def __init__(self, payload, headers=MessageHeaders()):
        if payload is None:
            raise RuntimeError("'payload cannot be None.")
        __check_supported_type__(payload)

        clazz =  type(MessageHeaders())
        if not type(headers) == clazz:
            raise RuntimeError("%s is an unsupported type for headers. Must be %s" % (type(headers), clazz))

        self.headers = headers
        self.payload = payload

    def __setattr__(self, key, value):
        if key == 'payload' or key == 'headers':
            try:
                self.__dict__[key]
                raise RuntimeError("Message is immutable")
            except KeyError:
                self.__dict__[key] = value
        else:
            raise RuntimeError("Attribute %s undefined" % value)

def __check_supported_type__(val):
    supported_types = [str,bool,bytearray,float,int,long]
    if not supported_types.__contains__(type(val)):
        raise RuntimeError("%s is an unsupported type" % type(val))
