#  Copyright (c) 2024 seamus@corvideon.ie
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
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging
import os
import time
import traceback
from typing import Any, Optional

from src.promptbouncer.config.api import PROMPT_BOUNCER_LOG_DIR
from src.promptbouncer.util.file_path_util import FilePathUtil

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s process:%(process)d %(levelname)s %(message)s",
)


class LoggingUtil:
    """
    Log to a local file, STDOUT and the python logger.
    """

    LOG_DIR = PROMPT_BOUNCER_LOG_DIR
    APP_LOG_SUFFIX = "_app.log"

    def __init__(self, prefix: Optional[str] = None) -> None:
        self.log_file_name: str = self.get_dated_log_file_name()
        self.log_file_dir: str = self.get_log_file_dir()
        self.check_and_create_log_dir()
        if prefix is None:
            self.prefix = ""
        else:
            self.prefix = prefix
            self.prefix = prefix

    def get_dated_log_file_name(self) -> str:
        return time.strftime("%Y%m%d-%H%M%S") + self.APP_LOG_SUFFIX

    def check_and_create_log_dir(self) -> None:
        try:
            if not os.path.exists(self.log_file_dir):
                os.makedirs(self.log_file_dir)
        except:  # noqa #nosec
            pass

    def log(self, log_message: str) -> None:
        # write to local log file
        t: Any = time.localtime()
        log: Any = open(self.get_log_file_path(), "a")
        log_string: str = time.asctime(t) + f"{self.prefix}: " + log_message
        log.write(log_string + "\n")
        log.close()

    def get_log_file_path(self) -> str:
        return os.path.join(self.log_file_dir, self.log_file_name)

    # noinspection PyMethodMayBeStatic
    def get_log_file_dir(self) -> str:
        return FilePathUtil.append_path_to_repo_path(self.LOG_DIR)

    def info(self, log_message: str) -> None:
        print(self.prefix + " " + log_message)
        logging.info(self.prefix + " " + log_message)
        self.log("INFO " + log_message)

    def debug(self, log_message: str) -> None:
        print(self.prefix + " " + log_message)
        logging.debug(self.prefix + " " + log_message)
        self.log("DEBUG " + log_message)

    def error(self, log_message: str) -> None:
        backtrace = traceback.format_exc()
        logging.error(self.prefix + " " + log_message)
        logging.error(backtrace)
        print(backtrace)
        print(self.prefix + " ERROR " + log_message)
        self.log("ERROR " + log_message)
        self.log(backtrace)

    @staticmethod
    def instance(prefix="") -> Any:
        return LoggingUtil(prefix=prefix)
