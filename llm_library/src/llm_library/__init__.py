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

"""
LLM Library - A standalone library for managing Large Language Model interactions.

This library provides:
- LLMMessages: Message management and building
- LLMClient: Base client for LLM providers 
- LLM: Facade for easy LLM interaction
- AdaptiveRequestMode: Parameter management for LLM requests
- Support for Instructor (structured outputs)
"""

from .llm_messages import LLMMessages
from .llm_client import LLMClient
from .llm_facade import LLM
from .adaptive_request_mode import AdaptiveRequestMode
from .llm_client_factory import LLMClientFactory
from .clients.openai import OpenAIClient
from .exceptions.llm_exception import LLMException

__version__ = "1.0.0"
__author__ = "seamus@corvideon.ie"

__all__ = [
    "LLMMessages",
    "LLMClient", 
    "LLM",
    "AdaptiveRequestMode",
    "LLMClientFactory",
    "OpenAIClient",
    "LLMException",
]