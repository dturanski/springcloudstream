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

import struct
import os,sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))


from springcloudstream.tcp.stream import Processor


def multiply(data):
    vals = struct.unpack('!if',data)
    return struct.pack('f',vals[0]*vals[1])

args =['--port','9999',
       '--monitor-port','9998',
       '--debug','True',
       '--encoder','L2'
       ]

Processor(multiply,args).start()
