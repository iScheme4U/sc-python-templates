# The MIT License (MIT)
#
# Copyright (c) 2025 Scott
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import logging

from sc_utilities import Config, Singleton, log_init

from . import PROJECT_NAME, __version__


class Runner(metaclass=Singleton):

    def __init__(self):
        project_name = PROJECT_NAME
        self._config = Config()

    def run(self, *, args):
        logging.getLogger(__name__).info("arguments {}".format(args))
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        logging.getLogger(__name__).debug("configurations {}".format(self._config))
        return 0


def main():
    try:
        log_init()
        parser = argparse.ArgumentParser(description='Python project')
        args = parser.parse_args()
        state = Runner().run(args=args)
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        return 1
    else:
        return state
