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

import unittest

from src.promptbouncer.api.bouncer import Bouncer


class TestBouncerEnum(unittest.TestCase):
    def test_low_threat_level(self):
        self.assertEqual(
            Bouncer.get_recommendation(1.0), Bouncer.Recommendation.OK_LET_THROUGH
        )
        self.assertEqual(
            Bouncer.get_recommendation(2.0), Bouncer.Recommendation.OK_LET_THROUGH
        )

    def test_moderate_threat_level(self):
        self.assertEqual(
            Bouncer.get_recommendation(3.0), Bouncer.Recommendation.INSPECT_THREATS
        )
        self.assertEqual(
            Bouncer.get_recommendation(4.0), Bouncer.Recommendation.INSPECT_THREATS
        )

    def test_elevated_threat_level(self):
        self.assertEqual(
            Bouncer.get_recommendation(5.0), Bouncer.Recommendation.INSPECT_THREATS
        )
        self.assertEqual(
            Bouncer.get_recommendation(6.0), Bouncer.Recommendation.INSPECT_THREATS
        )

    def test_high_threat_level(self):
        self.assertEqual(
            Bouncer.get_recommendation(7.0), Bouncer.Recommendation.STOP_NO_ENTRY
        )
        self.assertEqual(
            Bouncer.get_recommendation(8.0), Bouncer.Recommendation.STOP_NO_ENTRY
        )

    def test_critical_threat_level(self):
        self.assertEqual(
            Bouncer.get_recommendation(9.0), Bouncer.Recommendation.STOP_NO_ENTRY
        )
        self.assertEqual(
            Bouncer.get_recommendation(10.0), Bouncer.Recommendation.STOP_NO_ENTRY
        )

    def test_invalid_threat_level(self):
        with self.assertRaises(ValueError):
            Bouncer.get_recommendation(11.0)


if __name__ == "__main__":
    unittest.main()
