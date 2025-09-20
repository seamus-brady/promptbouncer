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

from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar, Union

import instructor
import litellm
from instructor import Partial
from litellm import completion as litellm_completion
from pydantic import BaseModel

from src.promptbouncer.exceptions.llm_exception import LLMException
from src.promptbouncer.llm.adaptive_request_mode import AdaptiveRequestMode
from src.promptbouncer.util.logging_util import LoggingUtil

# based on T in instructor.client.Instructor
T = TypeVar("T", bound=Union[BaseModel, Iterable, Partial])

# add tools use to the prompt for Non OpenAI LLMs
# see https://litellm.vercel.app/docs/completion/function_call
# litellm.add_function_to_prompt = True

# no logging thanks
litellm.telemetry = False


class LLMClient:
    """Base LLM client class."""

    LOGGER = LoggingUtil.instance("<LLMClient>")

    def __init__(self) -> None:
        self._model: Optional[str] = None

    @property
    def model(self) -> Optional[str]:
        return self._model

    def do_instructor(
        self,
        messages: List[Dict[str, str]],
        response_model: Type[T],
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Base method for calling Instructor completions.
        This patches the litellm completion object to allow the use of a response_model.
        Returns a full completion object.
        """
        LLMClient.LOGGER.debug("Starting instructor completion...")
        try:
            patched_client = instructor.from_litellm(litellm_completion)
            response = patched_client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=mode.max_tokens,
                temperature=mode.temperature,
                top_p=mode.top_p,
                response_model=response_model,
            )
            return response
        except Exception as error:
            LLMClient.LOGGER.error(str(error))
            raise LLMException(str(error))

    def do_tool(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List],
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Base method for calling tool using completions.
        Returns a full completion object.
        """
        LLMClient.LOGGER.debug("Starting tool completion...")
        try:
            response = litellm_completion(
                model=self.model,
                messages=messages,
                max_tokens=mode.max_tokens,
                temperature=mode.temperature,
                top_p=mode.top_p,
                tools=tools,
                tool_choice="auto",
            )
            return response
        except Exception as error:
            LLMClient.LOGGER.error(str(error))
            raise LLMException(str(error))

    def do_string(
        self,
        messages: List[Dict[str, str]],
        mode: AdaptiveRequestMode,
    ) -> str:
        """
        Base method for calling completions.
        Returns a string.
        """
        LLMClient.LOGGER.debug("Starting string completion...")
        try:
            response: Any = self.do_completion(messages=messages, mode=mode)
            return f"{response.choices[0].message.content}"
        except Exception as error:
            LLMClient.LOGGER.error(str(error))
            raise LLMException(str(error))

    def do_completion(
        self,
        messages: List[Dict[str, str]],
        mode: AdaptiveRequestMode,
    ) -> Any:
        """
        Base method for calling completions.
        Returns a full completion object.
        """
        LLMClient.LOGGER.debug("Starting completion...")
        try:
            response = litellm_completion(
                model=self.model,
                messages=messages,
                max_tokens=mode.max_tokens,
                temperature=mode.temperature,
                top_p=mode.top_p,
            )
            return response
        except Exception as error:
            LLMClient.LOGGER.error(str(error))
            raise LLMException(str(error))
