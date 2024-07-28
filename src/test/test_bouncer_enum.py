#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from src.promptbouncer.api.bouncer import Bouncer


class TestBouncerEnum(unittest.TestCase):
    def test_low_threat_level(self):
        self.assertEqual(Bouncer.get_recommendation(1.0), Bouncer.Recommendation.LET_THROUGH)
        self.assertEqual(Bouncer.get_recommendation(2.0), Bouncer.Recommendation.LET_THROUGH)

    def test_moderate_threat_level(self):
        self.assertEqual(Bouncer.get_recommendation(3.0), Bouncer.Recommendation.FRISK)
        self.assertEqual(Bouncer.get_recommendation(4.0), Bouncer.Recommendation.FRISK)

    def test_elevated_threat_level(self):
        self.assertEqual(Bouncer.get_recommendation(5.0), Bouncer.Recommendation.FRISK)
        self.assertEqual(Bouncer.get_recommendation(6.0), Bouncer.Recommendation.FRISK)

    def test_high_threat_level(self):
        self.assertEqual(Bouncer.get_recommendation(7.0), Bouncer.Recommendation.TURN_AWAY)
        self.assertEqual(Bouncer.get_recommendation(8.0), Bouncer.Recommendation.TURN_AWAY)

    def test_critical_threat_level(self):
        self.assertEqual(Bouncer.get_recommendation(9.0), Bouncer.Recommendation.TURN_AWAY)
        self.assertEqual(Bouncer.get_recommendation(10.0), Bouncer.Recommendation.TURN_AWAY)

    def test_invalid_threat_level(self):
        with self.assertRaises(ValueError):
            Bouncer.get_recommendation(11.0)


if __name__ == '__main__':
    unittest.main()
