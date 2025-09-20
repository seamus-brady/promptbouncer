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

#
from abc import ABC
from typing import Any

from src.promptbouncer.llm.llm_facade import LLM


class AbstractThreatScanner(ABC):
    """Abstract parent class for all threat scanners."""

    @staticmethod
    def scan(prompt: str) -> Any:
        raise NotImplementedError

    @staticmethod
    def is_filtered(prompt: str) -> bool:
        """Checks to see if a message has been filtered by the LLM"""
        if prompt is not None and prompt.__contains__(LLM.ERROR_FILTERED):
            return True
        else:
            return False
