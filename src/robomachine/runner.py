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
import os

import sys
import robomachine
import argparse

#Usage:
#  robomachine [OPTIONS] [INPUT.robomachine]
#
#Options:
# --tests-max NUMBER                    default 1000
# --steps-max NUMBER                    default 100
# --generation-algorithm (dfs|random)   default dfs
# --output NAME                         default INPUT.txt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RoboMachine, a test data generator for Robot Framework')
    parser.add_argument('input', type=str, help='input file')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='output file (default is input file with txt suffix)')
    parser.add_argument('--tests-max', '-t',
                         type=int, default=1000,
                         help='maximum number of tests to generate (default 1000)')
    parser.add_argument('--steps-max', '-s',
                         type=int, default=100,
                         help='maximum number of steps to generate (default 100)')
    parser.add_argument('--generation-algorithm', '-g',
                         type=str, default='dfs', choices=['dfs', 'random'],
                         help='used test generation algorithm (default dfs)')
    args = parser.parse_args()
    with open(args.input, 'r') as inp:
        with open(args.output or os.path.splitext(args.input)[0]+'.txt', 'w') as out:
            model = robomachine.parse(inp.read())
            robomachine.generate_all_dfs(model, args.steps_max, out)
