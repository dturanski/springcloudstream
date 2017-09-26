import random
import string
import unittest

from stdiotests.base import IOTestCase, getc

def random_data(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))+'\n'


class TestIOLf(IOTestCase):
    SERVER_NAME = 'io_echo_lf.py'

    def encode(self,s):
        ba = bytearray(s, 'utf-8')
        return ba

    def test_random_data(self):

        for i in range(10):
            func = lambda x,y: self.assertEqual(x[:-1], y)
            self.sendAndReceive(random_data(10), func)
            self.sendAndReceive(random_data(1025), func)
            self.sendAndReceive(random_data(2054), func)

    def test_multi_line(self):
        data = 'hello\nworld\nmulti\nline\ntests\n'
        self.send(data)
        for expected in data[:-1].split('\n'):
            actual = self.receive()
            self.assertEqual(expected, actual)

    def send(self,data):
        self.process.stdin.write(self.encode(data))
        self.process.stdin.flush()

    def receive(self):
        buf = bytearray()
        while True:
            c = getc(self.process)
            if not c:
                break
            if c == ord('\n'):
                return buf.decode('utf-8')
            buf.append(c)

    def sendAndReceive(self, data, func):
        self.send(data)
        result = self.receive()
        func(data, result)


if __name__ == 'main':
    unittest.main()
