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
import unittest

from dotenv import load_dotenv

from src.promptbouncer.llm.llm_facade import LLM
from src.promptbouncer.llm.llm_messages import LLMMessages

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


class TestLLMFacade(unittest.TestCase):
    def test_env_vars(self):
        openai_api_key = os.environ["OPENAI_API_KEY"]
        self.assertIsNotNone(openai_api_key)

    def test_llm_completion(self) -> None:
        llm: LLM = LLM()
        llm_messages = LLMMessages()
        llm_messages = llm_messages.build(
            "You are a helpful assistant.", llm_messages.SYSTEM
        )
        llm_messages = llm_messages.build("Knock knock.", llm_messages.USER)
        llm_messages = llm_messages.build("Who's there?", llm_messages.ASSISTANT)
        llm_messages = llm_messages.build("Orange.", llm_messages.USER)
        response: str = llm.do_completion(messages=llm_messages.messages)
        self.assertIsNotNone(response)
