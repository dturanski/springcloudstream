# springcloudstream
Python package to support streaming data to a Python application for use with [spring-cloud-stream](http://cloud.spring.io/spring-cloud-stream/). 
Python 2 and 3 are supported.

## Streaming API

* Processor (for send/receive messaging)

### TCP Implementation (springcloudstream.tcp)

This module uses raw TCP socket communications with supported encodings for both text oriented and binary data.  The `Processor` starts a 
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
                        the socket receive buffer size
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

This module utilizes a Google protocol buffers schema and associated gRPC service, defined below. This scheme is shared with the Spring Cloud Stream gRPC processor 
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
```
### Std I/O Implementation

This module  `stdin` and `stdout` to support another process piping data to it. Similar to the TCP implementation, the same Encoders are provided to support 
text or binary data.  

#### Std I/O Options
```
Options:
  -h, --help            show this help message and exit
  -c CHAR_ENCODING, --char-encoding=CHAR_ENCODING
                        character encoding
  -e ENCODER, --encoder=ENCODER
                        The name of the encoder to use for delimiting messages
  -d, --debug           turn on debug logging 
``` 

The `debug` option logs to `debug-timestamp.log` since any data written to `stdout` will be part of the stream. Avoid `print()` as well. 

#### Command Line Arguments

These modules use `optparse` to parse command line arguments. The OptionParser accepts additional command line arguments and returns left over arguments.
One caveat is that if leftover arguments look like options, i.e., prefixed with `--`, the parser will raise an `no such option` error. If your application
requires additional options, the work around is to precede them with a bare `--`. Examples:

```bash
$my_processor --knownoption foo some leftover args
$my_processor --knownoption foo -- --leftoveroption bar
```


The `springcloudstream.option` module provides a base class `OptionsParser` which wraps `optparse.OptionsParser()`. Each stream implementation subclasses this to
configure its options and provide a validation method. To access left over arguments (not formatted as options) you can use the module's `option_parser` class:

```python
import sys
from springcloudstream.tcp.stream import Processor
from springcloudstream.tcp.stream import options_parser

def echo(data):
    return data

'''Use the options_parser to extract your program args'''
opts,args =  options_parser.parse(sys.argv, validate=True)

'''Pass the tcp args to the processor'''
tcp_args = [x for x in sys.argv[1:] if x not in args]
Processor(echo,tcp_args).start()

```

To access proces arguments formatted as options, you can subclass the base `OptionsParser` class or use the standard `optparse.OptionParser` and declare your options first. 
For example `python myprocessor --foo foo --bar bar -- --buffer-size --host localhost --port 1234`

```python
import sys
from springcloudstream.tcp.stream import Processor
from springcloudstream.options import OptionsParser

class MyOptionsParser(OptionsParser):

    def __init__(self):
        OptionsParser.__init__(self)

        self.add_option('-f', '--foo',
                        help='foo option',
                        dest='foo')

        self.add_option('-b', '--bar',
                        help='bar option',
                        dest='bar')


opts,args = MyOptionsParser().parse(sys.argv) 

def func(data):
    if opts.foo == 'foo':
        return 'foo' + data
    else:
        return opts.bar + data
    
Processor(func, args).start()

```