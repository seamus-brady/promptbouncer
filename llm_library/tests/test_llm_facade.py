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

from llm_library.llm_facade import LLM
from llm_library.llm_messages import LLMMessages
from llm_library.adaptive_request_mode import AdaptiveRequestMode


class TestLLMFacade(unittest.TestCase):
    def test_llm_initialization(self):
        """Test that LLM facade can be initialized"""
        with patch('llm_library.llm_facade.LLMClientFactory.llm_client') as mock_factory:
            mock_client = Mock()
            mock_factory.return_value = mock_client
            
            llm = LLM()
            self.assertIsNotNone(llm)
            self.assertEqual(llm.wrapped_llm_client, mock_client)

    def test_llm_messages_integration(self):
        """Test that LLM facade works with LLMMessages"""
        llm_messages = LLMMessages()
        llm_messages = llm_messages.build("You are a helpful assistant.", llm_messages.SYSTEM)
        llm_messages = llm_messages.build("Hello!", llm_messages.USER)
        
        self.assertEqual(len(llm_messages.messages), 2)
        self.assertEqual(llm_messages.messages[0]["role"], "system")
        self.assertEqual(llm_messages.messages[1]["role"], "user")

    def test_is_bad_request(self):
        """Test the is_bad_request method"""
        with patch('llm_library.llm_facade.LLMClientFactory.llm_client') as mock_factory:
            mock_client = Mock()
            mock_factory.return_value = mock_client
            
            llm = LLM()
            
            # Test with 400 error
            error_400 = Exception("Error code: 400 - Bad Request")
            self.assertTrue(llm.is_bad_request(error_400))
            
            # Test with filtered response
            error_filtered = Exception("The response was filtered")
            self.assertTrue(llm.is_bad_request(error_filtered))
            
            # Test with normal error
            normal_error = Exception("Normal error")
            self.assertFalse(llm.is_bad_request(normal_error))


if __name__ == "__main__":
    unittest.main()