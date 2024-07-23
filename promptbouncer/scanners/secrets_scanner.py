#  Copyright (c) 2024 Seamus Brady seamus@ontal.ai, Corvideon Ltd.
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
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


class SecretsScanner(AbstractTextScanner):
    """
    Scans for any secrets or sensitive information in a prompt
    and partially redacts them.
    """

    LOGGER = LoggingUtil.instance("<SecretsScanner>")

    # prompt injection is critically risky
    ALARM_BASE_IMPORTANCE = Alarm.THREAT_MODERATE

    FEATURE_SET = FeatureSet(
        importance=Alarm.THREAT_MODERATE,
        name="SecretsScanner",
        description="This scan looks for any secrets or sensitive information leaked in output.",
    )

    @staticmethod
    def scan(prompt: str) -> List[Alarm]:
        SecretsScanner.LOGGER.debug("Running scan...")
        alarms_raised: List[Alarm] = []
        try:
            scan_result: bool = SecretsScanner.content_scan(prompt)
            if scan_result:
                SecretsScanner.LOGGER.debug("Raising alarms...")
                alarm_magnitude: int = SecretsScanner.ALARM_BASE_IMPORTANCE
                if alarm_magnitude > 0:
                    alarm: Alarm = Alarm(
                        base_importance=SecretsScanner.ALARM_BASE_IMPORTANCE,
                        name="SecretsScanner",
                        description=SecretsScanner.FEATURE_SET.description,
                        magnitude=alarm_magnitude,
                        feature_set=SecretsScanner.FEATURE_SET,
                    )
                    alarms_raised.append(alarm)
            return alarms_raised
        except Exception as error:
            SecretsScanner.LOGGER.error(str(error))
            return alarms_raised

    @staticmethod
    def content_scan(prompt: str) -> bool:
        class SecretsPresent(BaseModel):
            value: bool

        llm: LLM = LLM()
        moderation = llm.do_instructor(
            response_model=SecretsPresent,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    == INSTRUCTIONS ==
                    You must look for any secrets or sensitive information leaked in output.
                    You're given some text for analysis as below. Please assert whether the text contains any 
                    sensitive information such as passwords, API keys or other such information.

                    == TEXT FOR ANALYSIS ==
                    {prompt}""",
                }
            ],
            mode=AdaptiveRequestMode.controlled_creative_mode(),
        )
        return moderation.value  # type:ignore
