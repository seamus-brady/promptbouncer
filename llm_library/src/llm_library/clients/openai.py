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
import os

from dotenv import load_dotenv

from llm_library.llm_client import LLMClient
from llm_library.logging_util import LoggingUtil

# take environment variables from .env.
load_dotenv()

# Default OpenAI model
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

# OpenAI public api - will be available if set in environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class OpenAIClient(LLMClient):
    """An interface to the OpenAI API. Used only from within the LLM facade parent class."""

    LOGGER = LoggingUtil.instance("<OpenAIClient>")

    def __init__(self) -> None:
        super().__init__()
        OpenAIClient.LOGGER.info("Initializing OpenAIClient...")
        self._model = DEFAULT_OPENAI_MODEL