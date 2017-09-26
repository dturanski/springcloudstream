import random
import string
import unittest

from stdiotests.base import getc
from stdiotests.test_lf_encoding import TestIOLf

def random_data(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))+'\r\n'


class TestIOLf(TestIOLf):
    SERVER_NAME = 'io_echo_crlf.py'

    def encode(self,s):
        ba = bytearray(s, 'utf-8')
        return ba

    def test_random_data(self):

        for i in range(10):
            func = lambda x,y: self.assertEqual(x[:-2], y)
            self.sendAndReceive(random_data(10), func)
            self.sendAndReceive(random_data(1025), func)
            self.sendAndReceive(random_data(2054), func)

    def test_multi_line(self):
        data = 'hello\r\nworld\r\nmulti\r\nline\r\ntests\r\n'
        self.send(data)
        for expected in data[:-2].split('\r\n'):
            actual = self.receive()
            self.assertEqual(expected, actual)

    def receive(self):
        buf = bytearray()
        term = ''
        while True:
            c = getc(self.process)
            if not c:
                break
            if c == 13 or c == 10:
                term+=chr(c)
            else:
                buf.append(c)
            if term == '\r\n':
                return buf.decode('utf-8')


if __name__ == 'main':
    unittest.main()
