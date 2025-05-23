#  The MIT License (MIT)
#
#  Copyright (c) 2025 Scott
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
import logging

from sc_utilities import Config, log_init

from sc_templates import PROJECT_NAME, __version__, __build_date__


class MainAnalyzer:

    def __init__(self, config: Config):
        self._config = config

    def read_config(self):
        pass

    def validate(self):
        pass

    def analysis(self):
        logging.getLogger(__name__).info(f"program {PROJECT_NAME} version {__version__} build date {__build_date__}")
        logging.getLogger(__name__).debug("configurations {}".format(self._config))

        return 0


if __name__ == '__main__':
    log_init()
    analyzer = MainAnalyzer(Config())
    result = analyzer.analysis()
    logging.getLogger(__name__).info(f"结束分析，结果为: {result} ")
