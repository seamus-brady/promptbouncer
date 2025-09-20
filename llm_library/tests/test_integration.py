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
from unittest.mock import Mock, patch

from llm_library import LLMMessages, LLM, AdaptiveRequestMode, LLMException


class TestIntegration(unittest.TestCase):
    """Integration tests for the LLM Library components"""

    def test_llm_messages_and_modes(self):
        """Test LLMMessages works with different request modes"""
        messages = LLMMessages()
        messages = messages.build("You are a helpful assistant.", messages.SYSTEM)
        messages = messages.build("Hello!", messages.USER)
        
        # Test with different modes
        precision = AdaptiveRequestMode.precision_mode()
        balanced = AdaptiveRequestMode.balanced_mode()
        creative = AdaptiveRequestMode.controlled_creative_mode()
        
        self.assertEqual(len(messages.messages), 2)
        self.assertGreater(messages.token_count, 0)
        
        # Verify modes have correct settings
        self.assertEqual(precision.temperature, 0.2)
        self.assertEqual(balanced.temperature, 0.5)
        self.assertEqual(creative.temperature, 0.2)
        self.assertEqual(creative.top_p, 0.9)

    def test_full_library_import(self):
        """Test that all main components can be imported from the library"""
        from llm_library import (
            LLMMessages, LLM, AdaptiveRequestMode, 
            LLMClient, LLMClientFactory, OpenAIClient, LLMException
        )
        
        # Test instantiation
        messages = LLMMessages()
        mode = AdaptiveRequestMode()
        
        # Test constants
        self.assertEqual(messages.SYSTEM, "system")
        self.assertEqual(messages.USER, "user")
        self.assertEqual(messages.ASSISTANT, "assistant")

    def test_llm_with_mocked_client(self):
        """Test LLM facade with mocked client"""
        with patch('llm_library.llm_facade.LLMClientFactory.llm_client') as mock_factory:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Hello response"
            mock_client.do_string.return_value = "Hello response"
            mock_client.do_completion.return_value = mock_response
            mock_factory.return_value = mock_client
            
            llm = LLM()
            messages = LLMMessages()
            messages = messages.build("Hello", messages.USER)
            
            # Test string completion
            response = llm.do_string_completion(messages.messages)
            self.assertEqual(response, "Hello response")
            
            # Test completion
            response = llm.do_completion(messages.messages)
            self.assertEqual(response, mock_response)


if __name__ == "__main__":
    unittest.main()