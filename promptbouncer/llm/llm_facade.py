#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
#
#
#

from typing import Any, Dict, List, Optional, Type

from promptbouncer.exceptions.llm_exception import LLMException
from promptbouncer.llm.adaptive_request_mode import AdaptiveRequestMode
from promptbouncer.llm.llm_client import LLMClient, T
from promptbouncer.llm.llm_client_factory import LLMClientFactory
from promptbouncer.util.logging_util import LoggingUtil


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
