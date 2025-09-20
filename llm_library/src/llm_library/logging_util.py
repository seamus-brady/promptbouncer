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
import traceback
from typing import Any, Optional

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s process:%(process)d %(levelname)s %(message)s",
)


class LoggingUtil:
    """
    Simplified logging utility for standalone LLM library.
    """

    def __init__(self, prefix: Optional[str] = None) -> None:
        if prefix is None:
            self.prefix = ""
        else:
            self.prefix = prefix

    def info(self, log_message: str) -> None:
        print(self.prefix + " " + log_message)
        logging.info(self.prefix + " " + log_message)

    def debug(self, log_message: str) -> None:
        print(self.prefix + " " + log_message)
        logging.debug(self.prefix + " " + log_message)

    def error(self, log_message: str) -> None:
        backtrace = traceback.format_exc()
        logging.error(self.prefix + " " + log_message)
        logging.error(backtrace)
        print(backtrace)
        print(self.prefix + " ERROR " + log_message)

    @staticmethod
    def instance(prefix="") -> Any:
        return LoggingUtil(prefix=prefix)