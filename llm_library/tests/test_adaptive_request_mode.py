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

from llm_library.adaptive_request_mode import AdaptiveRequestMode


class TestAdaptiveRequestMode(unittest.TestCase):
    def test_default_initialization(self):
        """Test default initialization"""
        mode = AdaptiveRequestMode()
        self.assertEqual(mode.mode, AdaptiveRequestMode.Mode.BALANCED_MODE)
        self.assertEqual(mode.temperature, 0.5)
        self.assertEqual(mode.top_p, 0.5)
        self.assertEqual(mode.max_tokens, 4096)

    def test_precision_mode(self):
        """Test precision mode settings"""
        mode = AdaptiveRequestMode.precision_mode()
        self.assertEqual(mode.mode, AdaptiveRequestMode.Mode.PRECISION_MODE)
        self.assertEqual(mode.temperature, 0.2)
        self.assertEqual(mode.top_p, 0.1)
        self.assertEqual(mode.max_tokens, 4096)

    def test_controlled_creative_mode(self):
        """Test controlled creative mode settings"""
        mode = AdaptiveRequestMode.controlled_creative_mode()
        self.assertEqual(mode.mode, AdaptiveRequestMode.Mode.CONTROLLED_CREATIVE_MODE)
        self.assertEqual(mode.temperature, 0.2)
        self.assertEqual(mode.top_p, 0.9)
        self.assertEqual(mode.max_tokens, 4096)

    def test_dynamic_focused_mode(self):
        """Test dynamic focused mode settings"""
        mode = AdaptiveRequestMode.dynamic_focused_mode()
        self.assertEqual(mode.mode, AdaptiveRequestMode.Mode.DYNAMIC_FOCUSED_MODE)
        self.assertEqual(mode.temperature, 0.9)
        self.assertEqual(mode.top_p, 0.2)
        self.assertEqual(mode.max_tokens, 4096)

    def test_exploratory_mode(self):
        """Test exploratory mode settings"""
        mode = AdaptiveRequestMode.exploratory_mode()
        self.assertEqual(mode.mode, AdaptiveRequestMode.Mode.EXPLORATORY_MODE)
        self.assertEqual(mode.temperature, 0.9)
        self.assertEqual(mode.top_p, 0.9)
        self.assertEqual(mode.max_tokens, 4096)

    def test_balanced_mode(self):
        """Test balanced mode settings"""
        mode = AdaptiveRequestMode.balanced_mode()
        self.assertEqual(mode.mode, AdaptiveRequestMode.Mode.BALANCED_MODE)
        self.assertEqual(mode.temperature, 0.5)
        self.assertEqual(mode.top_p, 0.5)
        self.assertEqual(mode.max_tokens, 4096)

    def test_instance_method(self):
        """Test instance factory method"""
        mode = AdaptiveRequestMode.instance()
        self.assertEqual(mode.mode, AdaptiveRequestMode.Mode.BALANCED_MODE)


if __name__ == "__main__":
    unittest.main()