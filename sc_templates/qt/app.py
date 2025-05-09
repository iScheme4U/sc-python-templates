#  The MIT License (MIT)
#
#  Copyright (c) 2025 Scott Lau
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
import os
import queue
import threading
from logging.handlers import QueueHandler

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QFileDialog, QMessageBox
from sc_utilities import Config, SmartQueueHandler

from sc_templates import PROJECT_NAME, __version__, __build_date__
from sc_templates.analyzer.main_analyzer import MainAnalyzer
from sc_templates.log.log_worker import LogWorker


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._init_logging()

    def _init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(PROJECT_NAME)
        self.resize(800, 600)
        self._center_window()

        # 主窗口部件
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)

        # 主布局
        self._main_layout = QVBoxLayout(self._central_widget)
        self._main_layout.setContentsMargins(10, 10, 10, 10)
        self._main_layout.setSpacing(10)

        # 顶部文件选择框架
        self._create_top_frame()

        # 日志输出区域
        self._create_log_area()
        self._create_menu_bar()  # 新增菜单栏创建

    def _create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()

        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助(&H)")

        # 关于动作
        about_action = help_menu.addAction("关于(&A)")
        about_action.triggered.connect(self._show_about_dialog)

    def _show_about_dialog(self):
        """显示关于对话框"""

        about_msg = (
            f"{PROJECT_NAME}\n\n"
            f"版本: {__version__}\n"
            f"构建时间: {__build_date__}\n"
            f"Copyright © 2025 Scott Lau"
        )

        QMessageBox.information(
            self,
            "关于",
            about_msg,
            QMessageBox.StandardButton.Ok
        )

    def _center_window(self):
        """窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def _create_top_frame(self):
        """创建顶部文件选择框架"""
        top_frame = QFrame()
        top_frame.setFrameShape(QFrame.StyledPanel)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(5, 5, 5, 5)
        top_layout.setSpacing(10)

        # 路径标签
        path_label = QLabel("工作目录:")
        top_layout.addWidget(path_label)

        # 路径输入框
        self._path_edit = QLineEdit()
        self._path_edit.setPlaceholderText("请选择工作目录...")
        self._path_edit.setText(os.getcwd())
        top_layout.addWidget(self._path_edit, stretch=1)

        # 浏览按钮
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self._browse_directory)
        top_layout.addWidget(browse_btn)

        # 处理按钮
        self._process_btn = QPushButton("开始处理")
        self._process_btn.clicked.connect(self._processing)
        top_layout.addWidget(self._process_btn)

        # 清空按钮
        clear_btn = QPushButton("清空结果")
        clear_btn.clicked.connect(self._clear_output)
        top_layout.addWidget(clear_btn)

        self._main_layout.addWidget(top_frame)

    def _create_log_area(self):
        """创建日志输出区域"""
        log_label = QLabel("处理日志:")
        self._main_layout.addWidget(log_label)

        # 日志文本框
        self._output_area = QTextEdit()
        self._output_area.setReadOnly(True)
        self._output_area.setLineWrapMode(QTextEdit.WidgetWidth)
        self._output_area.setAcceptRichText(False)
        self._main_layout.addWidget(self._output_area, stretch=1)

    def _init_logging(self):
        """初始化日志系统"""
        self._buff_size = 1000
        self._log_queue = queue.Queue(maxsize=self._buff_size)
        self._log_flush_interval = 100  # 100毫秒刷新一次

        # 配置日志处理器
        queue_handler = SmartQueueHandler(self._log_queue)
        LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
        queue_handler.setLevel(LOG_LEVEL)

        root_logger = logging.getLogger()
        if not any(isinstance(h, QueueHandler) for h in root_logger.handlers):
            root_logger.addHandler(queue_handler)

        # 创建日志工作线程
        self._log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        self._log_worker = LogWorker(self._log_queue, self._log_formatter)
        self._log_worker._log_signal.connect(self._append_log)
        self._log_worker.start()

    def _load_config(self):
        self._config = Config()

    def _append_log(self, log):
        """追加日志到文本框"""
        self._output_area.moveCursor(QTextCursor.End)
        self._output_area.insertPlainText(log + "\n")

        # 自动滚动到底部
        self._output_area.ensureCursorVisible()

        # 清理旧日志
        line_count = self._output_area.document().lineCount()
        if line_count > 1500:
            cursor = self._output_area.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, line_count - 1000)
            cursor.removeSelectedText()

    def _browse_directory(self):
        """打开目录选择对话框"""
        initial_dir = self._path_edit.text() or os.getcwd()
        path = QFileDialog.getExistingDirectory(
            self,
            "选择工作目录",
            initial_dir,
            QFileDialog.ShowDirsOnly
        )

        if path:
            self._path_edit.setText(path)
            logging.getLogger(__name__).info(f"已选择工作目录: {path}")

    def _processing(self):
        """开始处理"""
        path = self._path_edit.text()

        # 验证路径
        if not path:
            QMessageBox.warning(self, "警告", "请先选择工作目录！")
            return

        if not os.path.isdir(path):
            QMessageBox.critical(self, "错误", "指定的路径不存在或不是目录！")
            return

        # 设置当前工作目录
        os.chdir(path)
        config_file = Config.DEFAULT_CONFIG_PATH
        if not os.path.exists(config_file):
            QMessageBox.critical(self, "错误", "配置文件不存在！")
            return
        logging.getLogger(__name__).info(f"当前工作目录已设置为: {path}")

        # 禁用处理按钮
        self._process_btn.setEnabled(False)

        # 启动处理线程
        self._processing_thread = threading.Thread(
            target=self._run,
            args=(),
            daemon=True,
            name="ProcessingThread"
        )
        self._processing_thread.start()

    def _clear_output(self):
        """清空文本框内容"""
        self._output_area.clear()

    def closeEvent(self, event):
        """重写关闭事件，确保资源释放"""
        self._log_worker.stop()
        super().closeEvent(event)

    def _run(self):
        self._process_btn.setEnabled(False)
        self._load_config()

        analyzer = MainAnalyzer(self._config)
        result = analyzer.analysis()
        self._process_btn.setEnabled(True)
        return result
