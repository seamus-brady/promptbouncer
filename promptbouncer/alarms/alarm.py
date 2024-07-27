#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
#
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict


@dataclass(frozen=True)
class Alarm:
    """
    Represents one alarm in the system.
    """

    THREAT_CRITICAL = 3
    THREAT_SERIOUS = 2
    THREAT_MODERATE = 1

    threat_level: int
    threat_details: str
    threat_scanner_name: str
    threat_scanner_description: str

    @staticmethod
    def get_threat_level_string(threat_level: int) -> str:
        if threat_level == 1:
            return "MODERATE"
        if threat_level == 2:
            return "SERIOUS"
        if threat_level == 3:
            return "CRITICAL"
        return "UNKNOWN"

    @staticmethod
    def calculate_threat_level(moderate: int, serious: int, critical: int) -> float:
        """A weighted sum of all the alarms"""

        weights = {1: 1, 2: 4, 3: 6}

        # calculate weighted sum
        weighted_sum = moderate * weights[1] + serious * weights[2] + critical * weights[3]
        total_alarms = moderate + serious + critical

        # calculate maximum possible weighted sum if all alarms were critical
        max_weighted_sum = total_alarms * weights[3]

        # no alarms
        if max_weighted_sum == 0:
            return 0

        # normalize the weighted sum to a scale of 0-10
        overall_threat_level = (weighted_sum / max_weighted_sum) * 10
        return overall_threat_level

    @staticmethod
    def count_threat_levels(alarms: List[Alarm]) -> Dict[int, int]:
        """Count alarms at level n"""
        counts = {1: 0, 2: 0, 3: 0}

        for alarm in alarms:
            threat_level = alarm.threat_level
            if threat_level in counts:
                counts[threat_level] += 1

        return counts