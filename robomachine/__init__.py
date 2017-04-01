#  Copyright 2011-2012 Mikko Korpela
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

try:
    from StringIO import StringIO
except:
    from io import StringIO

from robomachine.parsing import parse

from robomachine.version import VERSION
from robomachine.generator import Generator, DepthFirstSearchStrategy


__version__ = VERSION

def generate(machine, max_tests=1000, max_actions=None, to_state=None, output=None,
    strategy=DepthFirstSearchStrategy):
    generator = Generator()
    return generator.generate(machine, max_tests, max_actions, to_state, output, strategy)

def transform(text):
    output = StringIO()
    generate(parse(text), output=output)
    return output.getvalue()