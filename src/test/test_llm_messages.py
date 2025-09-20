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

import unittest

from src.promptbouncer.llm.llm_messages import LLMMessages


class TestLLMMessages(unittest.TestCase):
    def test_initialise(self):
        llm_messages = LLMMessages()
        self.assertIsNotNone(llm_messages.messages)

    def test_build(self):
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Knock knock."},
            {"role": "assistant", "content": "Who's there?"},
            {"role": "user", "content": "Orange."},
        ]
        messages = LLMMessages()
        # stupid python formatting screws up my nice builder pattern, this is easier to read
        messages = messages.build("You are a helpful assistant.", messages.SYSTEM)
        messages = messages.build("Knock knock.", messages.USER)
        messages = messages.build("Who's there?", messages.ASSISTANT)
        messages = messages.build("Orange.", messages.USER)
        self.assertEqual(test_messages, messages.messages)


if __name__ == "__main__":
    unittest.main()
