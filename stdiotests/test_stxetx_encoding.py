import random
import unittest

from stdiotests.base import IOTestCase, getc


def random_data(size):
    b=bytearray()
    for _ in range(size):
        b.append(random.choice(range(252)) + 4)
    return b

STX=2
ETX=3

class TestIOStxEtx(IOTestCase):
    SERVER_NAME = 'io_echo_stxetx.py'

    def encode(self,buf):
        ba = bytearray(buf)
        ba.insert(0,STX)
        ba.append(ETX)
        return ba

    def test_random_data(self):

        for i in range(10):
            func = lambda x,y: self.assertEqual(x, y[1:-1])
            self.sendAndReceive(random_data(10), func)
            self.sendAndReceive(random_data(1024), func)
            self.sendAndReceive(random_data(2054), func)

    # def test_multi_line(self):
    #     data = 'hello\nworld\nmulti\nline\ntests\n'
    #     self.send(data)
    #     for expected in data[:-1].split('\n'):
    #         actual = self.receive()
    #         self.assertEqual(expected, actual)

    def send(self,data):
        msg = self.encode(data)
        self.process.stdin.write(msg)
        self.process.stdin.flush()

    def receive(self):
        buf = bytearray()
        while True:
            c = getc(self.process)
            if not c:
                break
            buf.append(c)
            if c == ETX:
                return buf


    def sendAndReceive(self, data, func):
        self.send(data)
        result = self.receive()
        func(data, result)


if __name__ == 'main':
    unittest.main()
