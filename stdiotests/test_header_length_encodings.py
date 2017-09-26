import random
import unittest
import struct

from stdiotests.base import IOTestCase, getc
from springcloudstream.portability import PYTHON3


def random_data(size):
    b = bytearray()
    for _ in range(size):
        b.append(random.choice(range(255)))
    return b


class BaseTestCases:
    class TestIOHeaderLengthBase(IOTestCase):

        def encode(self, format, buf):
            ba = bytearray(struct.pack(format, len(buf)))
            if PYTHON3 and type(buf) == str:
                ba.extend(bytes(buf,'utf-8'))
            else:
                ba.extend(buf)

            return ba

        def test_text(self):
            self.sendAndReceive('hello', lambda x, y: self.assertEqual(x, y.decode('utf-8')))

        def test_random_data(self):
            SZ1, SZ2, SZ3 = 10, 1025, 2051

            if self.HEADER_LEN == 1:
                SZ1, SZ2, SZ3 = 10, 81, 255
            for i in range(10):
                func = lambda x, y: self.assertEqual(x, y)
            self.sendAndReceive(random_data(SZ1), func)
            self.sendAndReceive(random_data(SZ2), func)
            self.sendAndReceive(random_data(SZ3), func)

        def send(self, data):
            msg = self.encode(self.FORMAT, data)
            self.process.stdin.write(msg)
            self.process.stdin.flush()

        def receive(self):
            header = self.process.stdout.read(self.HEADER_LEN)
            data_size = self.data_size(header)

            buf = bytearray()
            for _ in range(data_size):
                c = getc(self.process)
                buf.append(c)
            return buf, data_size

        def sendAndReceive(self, data, func=None):
            self.send(data)
            result, size = self.receive()
            if func:
                func(data, result)

        def data_size(self, header):
            data_size = struct.unpack(self.FORMAT, header)[0]
            if self.FORMAT == 'B':
                data_size = ord(header)
            return data_size


class TestIOL2(BaseTestCases.TestIOHeaderLengthBase):
    SERVER_NAME = 'io_echo_l2.py'
    FORMAT = '!H'
    HEADER_LEN = 2


class TestIOL4(BaseTestCases.TestIOHeaderLengthBase):
    SERVER_NAME = 'io_echo_l4.py'
    FORMAT = '!I'
    HEADER_LEN = 4

class TestIOL1(BaseTestCases.TestIOHeaderLengthBase):
    SERVER_NAME = 'io_echo_l1.py'
    FORMAT = 'B'
    HEADER_LEN = 1


if __name__ == 'main':
    unittest.main()
