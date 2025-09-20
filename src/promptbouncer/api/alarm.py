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
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Alarm:
    """
    Represents one alarm in the system.
    """

    THREAT_CRITICAL = 3
    THREAT_SERIOUS = 2
    THREAT_MODERATE = 1

    # Dict { THREAT_MODERATE: 1, THREAT_SERIOUS: 2, THREAT_CRITICAL: 3}
    THREAT_WEIGHTS = {1: 1, 2: 2, 3: 3}

    threat_level: int
    threat_details: str
    threat_scanner_name: str
    threat_scanner_description: str
    confidence: float

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

        try:
            weights = Alarm.THREAT_WEIGHTS

            # calculate weighted sum
            weighted_sum = (
                moderate * weights[1] + serious * weights[2] + critical * weights[3]
            )
            total_alarms = moderate + serious + critical

            # calculate maximum possible weighted sum if all alarms were critical
            max_weighted_sum = total_alarms * weights[3]

            # no alarms
            if max_weighted_sum == 0:
                return 0

            # normalize the weighted sum to a scale of 0-10
            overall_threat_level = (weighted_sum / max_weighted_sum) * 10
            return overall_threat_level.__round__(2)
        except:  # noqa
            # if there are no threats, return nothing.
            return 0.0

    @staticmethod
    def calculate_overall_confidence(alarms: List[Alarm]) -> float:
        """A weighted average of all the alarm confidence levels"""
        try:
            if len(alarms) == 0:
                # no alarms, 100% confidence
                return 1.0

            total_weighted_score: float = 0.0
            total_weight: float = 0.0

            for alarm in alarms:
                weight = Alarm.THREAT_WEIGHTS[alarm.threat_level]
                total_weighted_score += weight * alarm.confidence
                total_weight += weight

            overall_confidence: float = total_weighted_score / total_weight

            return overall_confidence.__round__(2)
        except:  # noqa
            # if there is an error, return nothing.
            return 0.0

    @staticmethod
    def count_threat_levels(alarms: List[Alarm]) -> Dict[int, int]:
        """Count alarms at level n"""
        counts = {1: 0, 2: 0, 3: 0}

        for alarm in alarms:
            threat_level = alarm.threat_level
            if threat_level in counts:
                counts[threat_level] += 1

        return counts

    @staticmethod
    def get_threat_description(threat_level: float) -> str:
        """Gets a human-readable threat level"""
        if threat_level <= 2:
            return "Low threat level. The situation is under control."
        elif threat_level <= 4:
            return "Moderate threat level. There are some concerns."
        elif threat_level <= 6:
            return "Elevated threat level. Attention is required."
        elif threat_level <= 8:
            return "High threat level. Immediate action is advised."
        elif threat_level <= 10:
            return "Critical threat level. Urgent action is needed."
        else:
            return "Invalid threat level."
