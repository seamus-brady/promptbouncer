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
#
#

from typing import List

from pydantic import BaseModel
from src.ontal.core.cognition.forecast.feature import FeatureSet
from src.ontal.core.cycle.alarms.alarm import Alarm
from src.ontal.core.llm.llm_facade import LLM
from src.ontal.core.modes.adaptive_request_mode import AdaptiveRequestMode
from src.ontal.core.scanners.abstract_text_scanner import AbstractTextScanner
from src.ontal.util.logging_util import LoggingUtil


class LanguageDetectionScanner(AbstractTextScanner):
    """Scans for the use of languages other than EN in a prompt."""

    LOGGER = LoggingUtil.instance("<LanguageDetectionScanner>")

    ALARM_BASE_IMPORTANCE = Alarm.THREAT_MODERATE

    FEATURE_SET = FeatureSet(
        importance=Alarm.THREAT_MODERATE,
        name="LanguageDetectionScanner",
        description="This scan looks for attempted security issues in multiple languages.",
    )

    @staticmethod
    def scan(prompt: str) -> List[Alarm]:
        LanguageDetectionScanner.LOGGER.debug("Running scan...")
        alarms_raised: List[Alarm] = []
        try:
            multiple_langs: bool = LanguageDetectionScanner.language_scan(prompt)
            if multiple_langs:
                alarm_magnitude: int = Alarm.THREAT_MODERATE
                LanguageDetectionScanner.LOGGER.debug("Raising alarms...")
                alarm: Alarm = Alarm(
                    base_importance=LanguageDetectionScanner.ALARM_BASE_IMPORTANCE,  # noqa
                    name="LanguageDetectionScanner",
                    description=LanguageDetectionScanner.FEATURE_SET.description,
                    magnitude=alarm_magnitude,
                    feature_set=LanguageDetectionScanner.FEATURE_SET,
                )
                alarms_raised.append(alarm)
            return alarms_raised
        except Exception as error:
            LanguageDetectionScanner.LOGGER.error(str(error))
            return alarms_raised

    @staticmethod
    def language_scan(prompt: str) -> bool:
        class MultipleLanguagesPresent(BaseModel):
            value: bool

        llm: LLM = LLM()
        multiple_langs = llm.do_instructor(
            response_model=MultipleLanguagesPresent,
            messages=[
                {
                    "role": "user",
                    "content": f"Are there languages other than English present in this string?: {prompt}",
                }
            ],
            mode=AdaptiveRequestMode.controlled_creative_mode(),
        )
        return multiple_langs.value  # type:ignore
