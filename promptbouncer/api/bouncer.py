#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import annotations

from enum import Enum
from typing import Dict, List

from promptbouncer.api.alarm import Alarm
from promptbouncer.api.entities import Threat, ThreatAssessment
from promptbouncer.api.threat_scan import ThreatScan
from promptbouncer.exceptions.api_exception import APIException
from promptbouncer.util.logging_util import LoggingUtil


class Bouncer:
    """Provides a security service for the doorway of your LLM app."""

    LOGGER = LoggingUtil.instance("<Bouncer>")

    class Recommendation(str, Enum):
        """A recommendation on what to do with a prompt."""

        LET_THROUGH = "LET_THROUGH"
        FRISK = "FRISK"
        TURN_AWAY = "TURN_AWAY"

    def __init__(self):
        """Not needed."""
        pass

    @staticmethod
    def door_check(incoming_prompt: str) -> ThreatAssessment:
        """Does a threat assessment of an incoming prompt. Returns a threat assessment."""

        try:
            alarms: List[Alarm] = ThreatScan.instance().run(incoming_prompt)
            threats: List[Threat] = []
            for alarm in alarms:
                threats.append(
                    Threat(
                        threat_scan=alarm.threat_scanner_name,
                        threat_scan_description=alarm.threat_scanner_description,
                        threat_level=Alarm.get_threat_level_string(alarm.threat_level),
                        threat_details=alarm.threat_details,
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
            return ThreatAssessment(
                threats=threats,
                assessment_score=assessment_score,
                assessment_description=assessment_description,
                recommendation=Bouncer.get_recommendation(assessment_score),
            )
        except Exception as error:
            Bouncer.LOGGER.error(error.__str__())
            raise APIException(error.__str__())

    @staticmethod
    def get_recommendation(threat_level: float) -> Bouncer.Recommendation:
        if threat_level <= 2:
            return Bouncer.Recommendation.LET_THROUGH
        elif threat_level <= 6:
            return Bouncer.Recommendation.FRISK
        elif threat_level <= 10:
            return Bouncer.Recommendation.TURN_AWAY
        else:
            raise ValueError("Invalid threat level")
