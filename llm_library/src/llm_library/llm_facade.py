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
#
#
#

from typing import Any, Dict, List, Type

from llm_library.exceptions.llm_exception import LLMException
from llm_library.adaptive_request_mode import AdaptiveRequestMode
from llm_library.llm_client import LLMClient, T
from llm_library.llm_client_factory import LLMClientFactory
from llm_library.logging_util import LoggingUtil


class LLM:
    """A facade for communicating with various LLMs."""

    ERROR_FILTERED = "400 ERROR - FILTERED"
    BAD_REQUEST = "Prompt was filtering by LLM and triggered a 400 <Bad Request>."
    LOGGER = LoggingUtil.instance("<LLM>")

    def __init__(self) -> None:
        try:
            self._wrapped_llm_client = LLMClientFactory.llm_client()
        except Exception as error:
            raise LLMException(str(error))

    @property
    def wrapped_llm_client(self) -> LLMClient:
        return self._wrapped_llm_client

    def do_instructor(
        self,
        messages: List[Dict[str, str]],
        response_model: Type[T],
        mode: AdaptiveRequestMode = AdaptiveRequestMode.instance(),
    ) -> Any:
        try:
            completion: Any = self.wrapped_llm_client.do_instructor(
                messages=messages, response_model=response_model, mode=mode
            )
            return completion
        except Exception as error:
            LLM.LOGGER.error(str(error))
            if self.is_bad_request(error):
                LLM.LOGGER.error(self.BAD_REQUEST)
                return LLM.ERROR_FILTERED
            else:
                # all other errors
                raise LLMException(str(error))

    def do_completion(
        self,
        messages: List[Dict[str, str]],
        mode: AdaptiveRequestMode = AdaptiveRequestMode.instance(),
    ) -> Any:
        try:
            completion: str = self.wrapped_llm_client.do_completion(
                messages=messages, mode=mode
            )
            return completion
        except Exception as error:
            LLM.LOGGER.error(str(error))
            if self.is_bad_request(error):
                LLM.LOGGER.error(self.BAD_REQUEST)
                return LLM.ERROR_FILTERED
            else:
                # all other errors
                raise LLMException(str(error))

    def do_string_completion(
        self,
        messages: List[Dict[str, str]],
        mode: AdaptiveRequestMode = AdaptiveRequestMode.instance(),
    ) -> str:
        try:
            completion: str = self.wrapped_llm_client.do_string(
                messages=messages, mode=mode
            )
            return completion
        except Exception as error:
            LLM.LOGGER.error(str(error))
            if self.is_bad_request(error):
                LLM.LOGGER.error(self.BAD_REQUEST)
                return LLM.ERROR_FILTERED
            else:
                # all other errors
                raise LLMException(str(error))

    # noinspection PyMethodMayBeStatic
    def is_bad_request(self, error):
        return error.args is not None and (
            str(error.args[0]).__contains__("Error code: 400")
            or (str(error.args[0]).__contains__("The response was filtered"))
            or str(error.args[0]).__contains__("input_value='content_filter'")
        )