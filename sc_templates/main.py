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
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMessageBox)
from sc_utilities import log_init

from sc_templates.qt.app import Application


def main():
    try:
        log_init()
        # 创建Qt应用
        app = QApplication([])

        # 设置高DPI支持
        app.setAttribute(Qt.AA_EnableHighDpiScaling)

        # 创建主窗口
        window = Application()
        window.show()

        # 执行应用
        return app.exec()
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        QMessageBox.critical(None, "错误", f"程序出错了！错误信息：{e}")
        return 1
