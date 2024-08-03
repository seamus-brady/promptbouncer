#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import unittest

from src.promptbouncer.api.alarm import Alarm


class TestAlarm(unittest.TestCase):
    def test_get_threat_level_string(self):
        self.assertEqual(Alarm.get_threat_level_string(1), "MODERATE")
        self.assertEqual(Alarm.get_threat_level_string(2), "SERIOUS")
        self.assertEqual(Alarm.get_threat_level_string(3), "CRITICAL")
        self.assertEqual(Alarm.get_threat_level_string(0), "UNKNOWN")

    def test_calculate_threat_level(self):
        self.assertAlmostEqual(Alarm.calculate_threat_level(1, 1, 1), 6.67)
        self.assertAlmostEqual(Alarm.calculate_threat_level(0, 0, 0), 0.0)
        self.assertAlmostEqual(Alarm.calculate_threat_level(0, 0, 1), 10.0)
        self.assertAlmostEqual(Alarm.calculate_threat_level(1, 0, 0), 3.33)

    def test_count_threat_levels(self):
        alarms = [
            Alarm(1, "Details1", "Scanner1", "Description1", 1.0),
            Alarm(2, "Details2", "Scanner2", "Description2", 1.0),
            Alarm(3, "Details3", "Scanner3", "Description3", 1.0),
            Alarm(1, "Details4", "Scanner4", "Description4", 1.0),
        ]
        self.assertEqual(Alarm.count_threat_levels(alarms), {1: 2, 2: 1, 3: 1})

    def test_confidence_calc(self):
        alarms = [
            Alarm(1, "Details1", "Scanner1", "Description1", 0.5),
            Alarm(2, "Details2", "Scanner2", "Description2", 1.0),
            Alarm(3, "Details3", "Scanner3", "Description3", 6.7),
            Alarm(1, "Details4", "Scanner4", "Description4", 8.6),
        ]
        self.assertEqual(Alarm.calculate_overall_confidence(alarms), 4.46)

    def test_get_threat_description(self):
        self.assertEqual(
            Alarm.get_threat_description(1.0),
            "Low threat level. The situation is under control.",
        )
        self.assertEqual(
            Alarm.get_threat_description(3.0),
            "Moderate threat level. There are some concerns.",
        )
        self.assertEqual(
            Alarm.get_threat_description(5.0),
            "Elevated threat level. Attention is required.",
        )
        self.assertEqual(
            Alarm.get_threat_description(7.0),
            "High threat level. Immediate action is advised.",
        )
        self.assertEqual(
            Alarm.get_threat_description(9.0),
            "Critical threat level. Urgent action is needed.",
        )
        self.assertEqual(Alarm.get_threat_description(11.0), "Invalid threat level.")


if __name__ == "__main__":
    unittest.main()
