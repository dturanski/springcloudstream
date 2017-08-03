# springcloudstream
Python package to support streaming data over gRPC for use with [spring-cloud-stream](http://cloud.spring.io/spring-cloud-stream/). 
Python 2 and 3 are supported.

## Streaming API

* Processor (for send/receive)

This package utilizes a Google protobuf schema and associated gRPC service shared with the Spring Cloud Stream gRPC processor which 
supports interoperability of Spring Cloud Stream application with a service written in any language that gRPC supports. The `Processor` 
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


## Example

```python
from springcloudstream.grpc.stream import Processor

def echo(data):
    return data


Processor(echo, sys.argv).start()

```

Note `sys.argv` as the 2nd parameter. This can be any list including the following options:

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








