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


import sys
import inspect

PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
    long = int
    getfullargspec = inspect.getfullargspec
    def __is_str_type__(val):
        return isinstance(val,str)
else:
    long = long
    getfullargspec = inspect.getargspec
    def __is_str_type__(val):
        return isinstance(val, basestring)