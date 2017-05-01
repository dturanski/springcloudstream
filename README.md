# springcloudstream
Python package to support streaming data over stdin and stdout for use with [spring-cloud-stream](http://cloud.spring.io/spring-cloud-stream/).

## Streaming API

* Processor (for senc/receive)
* Sink (for send only)

## Example

```python
from springcloudstream.stream import Processor

def echo(data):
    return data


processor = Processor()
processor.start(echo)

```

## Encoders

The following encoders (message delimiters) are supported: 

* `CRLF` - (`\r\n` - default)
* `LF` - (`\n`)
* `BINARY` -  (`\a1x\`) 

Example: 

```python
from springcloudstream.stream import Processor, Encoders

def echo(data):
    return data


processor = Processor(Encoders.BINARY)
processor.start(echo)
