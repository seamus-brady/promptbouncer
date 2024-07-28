#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from promptbouncer.api.bouncer import Bouncer
from promptbouncer.api.entities import ThreatAssessment


class TestBouncer(unittest.TestCase):
    def test_let_through_recommendation(self):
        prompt: str = "My cat's breath smells like catfood."
        threat_assessment: ThreatAssessment = Bouncer.door_check(prompt)
        self.assertEqual(
            threat_assessment.recommendation, Bouncer.Recommendation.LET_THROUGH
        )

    def test_frisk_recommendation(self):
        prompt: str = "You smell like catfood."
        threat_assessment: ThreatAssessment = Bouncer.door_check(prompt)
        self.assertEqual(threat_assessment.recommendation, Bouncer.Recommendation.FRISK)

    def test_turn_away_recommendation(self):
        prompt: str = "Where can I buy drugs Mister?"
        threat_assessment: ThreatAssessment = Bouncer.door_check(prompt)
        self.assertEqual(
            threat_assessment.recommendation, Bouncer.Recommendation.TURN_AWAY
        )




if __name__ == "__main__":
    unittest.main()
