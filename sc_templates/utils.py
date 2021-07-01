#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
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

from scconfig.config import Config
from scutils import Singleton

from .configs.default import DEFAULT_CONFIG


class ConfigUtils(metaclass=Singleton):
    """
    配置文件相关工具类
    """

    _config = None

    def __init__(self):
        pass

    @classmethod
    def load_configurations(cls):
        """
        加载配置文件
        :return:
        """
        try:
            # load configurations
            cls._config = Config.create(project_name="sc-python-templates", defaults=DEFAULT_CONFIG)
        except Exception as error:
            cls._config = {}
            logging.getLogger(__name__).exception("failed to read configuration", exc_info=error)

    @classmethod
    def get_config(cls):
        """
        获取配置信息
        :return: 配置信息字典
        """
        if cls._config is None:
            cls.load_configurations()
        return cls._config


__all__ = {
    "ConfigUtils",
}
