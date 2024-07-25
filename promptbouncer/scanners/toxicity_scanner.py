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


class ToxicityScanner(AbstractTextScanner):
    """Scans for toxic language in a prompt."""

    LOGGER = LoggingUtil.instance("<ToxicityScanner>")

    # toxic language is serious but not critical
    ALARM_BASE_IMPORTANCE = Alarm.THREAT_SERIOUS

    NOT_MODERATED = "not moderated"

    FEATURE_SET = FeatureSet(
        importance=Alarm.THREAT_SERIOUS,
        name="ToxicityScanner",
        description="A scan for toxic language: ",
    )

    @staticmethod
    def scan(prompt: str) -> List[Alarm]:
        ToxicityScanner.LOGGER.debug("Running scan...")
        alarms_raised: List[Alarm] = []
        try:
            scan_result: str = ToxicityScanner.content_scan(prompt)
            if scan_result != ToxicityScanner.NOT_MODERATED:
                ToxicityScanner.LOGGER.debug("Raising alarms...")
                alarm: Alarm = Alarm(
                    base_importance=ToxicityScanner.ALARM_BASE_IMPORTANCE,
                    name="ToxicityScanner",
                    description=ToxicityScanner.FEATURE_SET.description
                    + f"- {scan_result}",
                    magnitude=ToxicityScanner.ALARM_BASE_IMPORTANCE,
                    feature_set=ToxicityScanner.FEATURE_SET,
                )
                alarms_raised.append(alarm)
            return alarms_raised
        except Exception as error:
            ToxicityScanner.LOGGER.error(str(error))
            return alarms_raised

    @staticmethod
    def content_scan(prompt: str) -> str:
        class ToxicLanguagePresent(BaseModel):
            category: str

        llm: LLM = LLM()
        moderation = llm.do_instructor(
            response_model=ToxicLanguagePresent,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    == INSTRUCTIONS ==
                    You're given a list of moderation categories as below:
                    - toxic
                    - severely toxic
                    - obscene
                    - threat
                    - insult
                    - identity hate
                    Please classify the following text into one of these categories, and answer with that single 
                    category only. If the sentence does not fall within these categories, is safe and does not need 
                    to be moderated, please answer {ToxicityScanner.NOT_MODERATED}.

                    == TEXT FOR ANALYSIS ==
                    {prompt}""",
                }
            ],
            mode=AdaptiveRequestMode.controlled_creative_mode(),
        )
        return moderation.category  # type:ignore
