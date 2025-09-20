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

from __future__ import annotations

import time
from enum import Enum
from typing import Dict, List

from src.promptbouncer.api.alarm import Alarm
from src.promptbouncer.api.entities import Threat, ThreatAssessment
from src.promptbouncer.api.threat_scan import ThreatScan
from src.promptbouncer.exceptions.api_exception import APIException
from src.promptbouncer.util.logging_util import LoggingUtil


class Bouncer:
    """Provides a security service for the doorway of your LLM app."""

    LOGGER = LoggingUtil.instance("<Bouncer>")

    class Recommendation(str, Enum):
        """A recommendation on what to do with a prompt."""

        OK_LET_THROUGH = "OK_LET_THROUGH"
        INSPECT_THREATS = "INSPECT_THREATS"
        STOP_NO_ENTRY = "STOP_NO_ENTRY"

    def __init__(self):
        """Not needed."""
        pass

    @staticmethod
    def do_threat_assessment(incoming_prompt: str) -> ThreatAssessment:
        """Does a threat assessment of an incoming prompt. Returns a threat assessment."""

        try:
            start_time: float = time.time()
            alarms: List[Alarm] = ThreatScan.instance().run(incoming_prompt)
            threats: List[Threat] = []
            for alarm in alarms:
                threats.append(
                    Threat(
                        threat_scan=alarm.threat_scanner_name,
                        threat_scan_description=alarm.threat_scanner_description,
                        threat_level=Alarm.get_threat_level_string(alarm.threat_level),
                        threat_details=alarm.threat_details,
                        confidence=alarm.confidence,
                    )
                )

            threat_level_count_dict: Dict[int, int] = Alarm.count_threat_levels(
                alarms=alarms
            )

            assessment_score = Alarm.calculate_threat_level(
                threat_level_count_dict[Alarm.THREAT_MODERATE],
                threat_level_count_dict[Alarm.THREAT_SERIOUS],
                threat_level_count_dict[Alarm.THREAT_CRITICAL],
            )

            assessment_description = Alarm.get_threat_description(assessment_score)
            assessment_confidence = Alarm.calculate_overall_confidence(alarms)
            end_time = time.time()
            elapsed_time = end_time - start_time
            return ThreatAssessment(
                threats=threats,
                assessment_score=assessment_score,
                assessment_description=assessment_description,
                assessment_confidence=assessment_confidence,
                recommendation=Bouncer.get_recommendation(assessment_score),
                time_taken_seconds=elapsed_time.__round__(2),
            )
        except Exception as error:
            Bouncer.LOGGER.error(error.__str__())
            raise APIException(error.__str__())

    @staticmethod
    def get_recommendation(threat_level: float) -> Bouncer.Recommendation:
        if threat_level <= 2:
            return Bouncer.Recommendation.OK_LET_THROUGH
        elif threat_level <= 6:
            return Bouncer.Recommendation.INSPECT_THREATS
        elif threat_level <= 10:
            return Bouncer.Recommendation.STOP_NO_ENTRY
        else:
            raise ValueError("Invalid threat level")
