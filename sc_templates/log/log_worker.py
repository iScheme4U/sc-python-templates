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
import queue

from PySide6.QtCore import QThread, Signal


class LogWorker(QThread):
    """日志工作线程，继承自QThread"""
    _log_signal = Signal(str)  # 定义信号，用于向主线程传递日志

    def __init__(self, log_queue, formatter, parent=None):
        super().__init__(parent)
        self._log_queue = log_queue
        self._formatter = formatter
        self._running = True

    def run(self):
        """线程主循环"""
        while self._running:
            try:
                record = self._log_queue.get(timeout=0.05)
                formatted_log = self._formatter.format(record)
                self._log_signal.emit(formatted_log)  # 发射信号
            except queue.Empty:
                continue

    def stop(self):
        """停止线程"""
        self._running = False
        self.wait()
