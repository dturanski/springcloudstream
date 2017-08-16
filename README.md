# springcloudstream
Python package to support streaming data to a Python application for use with [spring-cloud-stream](http://cloud.spring.io/spring-cloud-stream/). 
Python 2 and 3 are supported.

## Streaming API

* Processor (for send/receive messaging)

### TCP Implementation (springcloudstream.tcp)

Uses raw TCP socket communications with supported encodings for both text oriented and binary data.  The `Processor` starts a 
socket server using to wrap a user defined function providing a single argument containing the contents of the message payload and 
returning the result. 


#### Example

```python
import sys
from springcloudstream.tcp.stream import Processor

def echo(data):
    return data

Processor(echo, sys.argv).start()

```

#### TCP Options
Options:
  -h, --help            show this help message and exit
  -p PORT, --port=PORT  the socket port to use
  -m MONITOR_PORT, --monitor-port=MONITOR_PORT
                        the socket to use for the monitoring server
  -s BUFFER_SIZE, --buffer-size=BUFFER_SIZE
                        the tcp buffer size
  -d, --debug           turn on debug logging
  -c CHAR_ENCODING, --char-encoding=CHAR_ENCODING
                        character encoding
  -e ENCODER, --encoder=ENCODER
                        The name of the encoder to use for delimiting messages

#### Encoders

The following encoders (message delimiters) are supported: 
* For text messages
    * `CRLF` - (`\r\n` - default)
    * `LF` - (`\n`)

* For binary data
    * `L1,L2, L4` - n byte header containing message length
    * `STXETX` -  Start (`0x2`) and End(`0x3`) transmission delimiters 

Example: 

```python
import sys
from springcloudstream.tcp.stream import Processor


def echo(data):
    return data

'''
Normally use sys.argv instead of hard coding args
'''    
args =['--port','9999',
       '--monitor-port','9998',
       '--debug','True',
       '--encoder','L4']

Processor(echo,args).start()

```

### Grpc Implementation (springcloudstream.grpc)

This package utilizes a Google protocol buffers schema and associated gRPC service, defined below. This scheme is shared with the Spring Cloud Stream gRPC processor 
to support interoperability of Spring Cloud Stream application with a service written in any language that gRPC supports. The `Processor` 
starts a gRPC server to wrap a user defined function.

The gRPC `Processor` service is defined as follows:

```
service Processor {
  rpc Ping(google.protobuf.Empty) returns (Status) {}
  rpc Process(message.Message) returns (message.Message) {}
}
```

Where `Ping` is used by the client application to check the health of the service, and `Process` wraps the provided function to process 
messages. The `Message` type models a Spring [Message](http://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/messaging/Message.html).
Which includes a `payload` and `headers`.  Here `payload` may be any primitive (scalar) type, `str`, `bytes`, or `unicode` type.  Message headers are represented 
as a `map` or `dict` and contain additional metadata about the message. Normally, you don't need to worry about headers. In some cases applications may add custom header 
values used during message processing. 

This package uses a simple convention. Your function must have one or two arguments. If one, it will contain the message payload, if two, the first argument is the payload
and the second argument is the headers. If you set any headers, you must return a Message type, otherwise the return value is the payload of the message returned to the client
application.

#### Grpc Options

```
Options:
  -h, --help            show this help message and exit
  -p PORT, --port=PORT  the socket port to use
  -t THREAD_POOL_SIZE, --thread-pool-size=THREAD_POOL_SIZE
                        the thread pool size
  -m MAX_CONCURRENT_RPCS, --max-concurrent-rpcs=MAX_CONCURRENT_RPCS
                        the max concurrent RPCs
  -d, --debug           turn on debug logging 

```

where `port` is required. Typically these are passed on the command line:

`python echo.py --port=9999 --debug`
```

#### Example

```python
import sys
from springcloudstream.grpc.stream import Processor

def echo(data):
    return data

Processor(echo, sys.argv).start()

