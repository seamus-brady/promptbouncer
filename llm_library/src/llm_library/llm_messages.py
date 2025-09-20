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
from typing import TYPE_CHECKING, Any, Dict, List, cast

from llm_library.exceptions.llm_exception import LLMException
from llm_library.logging_util import LoggingUtil

# Optional token estimation - will gracefully fall back if not available
try:
    from openai_function_tokens import estimate_tokens
    TOKEN_ESTIMATION_AVAILABLE = True
except (ImportError, Exception):
    # Catch any exception including network errors during tiktoken initialization
    TOKEN_ESTIMATION_AVAILABLE = False
    def estimate_tokens(messages: List[Dict[str, str]]) -> int:
        """Fallback token estimation based on character count"""
        total_chars = sum(len(str(msg.get('content', ''))) for msg in messages)
        return max(1, total_chars // 4)  # Rough approximation: 4 chars ≈ 1 token

if TYPE_CHECKING:
    from typing import Self
else:
    Self = Any


class LLMMessages:
    """A class for managing prompts."""

    LOGGER = LoggingUtil.instance("<LLMMessages>")

    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"

    def __init__(self) -> None:
        self._messages: List[Dict[str, str]] = []

    @property
    def messages(self) -> List[Dict[str, str]]:
        return self._messages

    @messages.setter
    def messages(self, new_messages: List[Dict[str, str]]) -> None:
        self._messages = new_messages.copy()

    @property
    def token_count(self) -> int:
        return cast(int, estimate_tokens(self.messages))

    # noinspection PyMethodMayBeStatic
    def build_user_prompt(self, content: str) -> Dict[str, str]:
        return {"role": "user", "content": content}

    # noinspection PyMethodMayBeStatic
    def build_assistant_prompt(self, content: str) -> Dict[str, str]:
        return {"role": "assistant", "content": content}

    # noinspection PyMethodMayBeStatic
    def build_system_prompt(self, content: str) -> Dict[str, str]:
        return {"role": "system", "content": content}

    # noinspection PyMethodMayBeStatic
    def build_tool_prompt(
        self, tool_call: Any, function_name, content: str
    ) -> Dict[str, str]:
        return {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": f"{content}",
        }

    def build(
        self,
        content: str,
        content_type: str,
    ) -> Self:
        try:
            if content_type == self.SYSTEM:
                message = self.build_system_prompt(content)
                self.messages.append(message)
            if content_type == self.USER:
                message = self.build_user_prompt(content)
                self.messages.append(message)
            if content_type == self.ASSISTANT:
                message = self.build_assistant_prompt(content)
                self.messages.append(message)
            return self
        except Exception as error:
            LLMMessages.LOGGER.error(str(error))
            raise LLMException(str(error))