__copyright__ = """
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
"""

import sys
import os
import unittest
import subprocess
import signal
import time

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
    PY_COMMAND = 'python3'

if PYTHON3:
    def getc(proc):
        c, = proc.stdout.read(1)
        return c
else:
    PY_COMMAND = 'python'


    def getc(proc):
        c = proc.stdout.read(1)
        return ord(c)


class IOTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SERVER = '%s/%s' % (cls.servers_root(), cls.SERVER_NAME)

        cls.process = subprocess.Popen(
            '%s -u %s' % (PY_COMMAND, SERVER),
            shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE, stdin=subprocess.PIPE
        )
        time.sleep(1.0)

    @classmethod
    def tearDownClass(cls):
        try:
            os.killpg(cls.process.pid, signal.SIGTERM)
        except:
            print("ERROR: Unable to kill PID %d" % cls.process.pid)

    @classmethod
    def servers_root(cls):
        return '%s/servers' % os.path.dirname(__file__)
