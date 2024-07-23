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
from typing import Any, List

from src.ontal.core.cognition.forecast.feature import FeatureSet
from src.ontal.core.cycle.alarms.alarm import Alarm
from src.ontal.core.llm.llm_facade import LLM
from src.ontal.core.llm.llm_messages import LLMMessages
from src.ontal.core.modes.adaptive_request_mode import AdaptiveRequestMode
from src.ontal.core.scanners.abstract_text_scanner import AbstractTextScanner
from src.ontal.util.logging_util import LoggingUtil


class PromptHijackScanner(AbstractTextScanner):
    """
    A class to check prompt hijacking. If the response does not contain the canary,
    this may indicate goal hijacking prompt injection
    Based on https://vigil.deadbits.ai/overview/use-vigil/scanners/canary-tokens
    """

    LOGGER = LoggingUtil.instance("<PromptHijackScanner>")

    CANARY_STRING: str = "1cbbe75d8cf4a0ce"

    # prompts hijacks are critical
    ALARM_BASE_IMPORTANCE = Alarm.THREAT_CRITICAL

    FEATURE_SET = FeatureSet(
        importance=Alarm.THREAT_CRITICAL,
        name="PromptHijackScanner",
        description="A scan to check prompt hijacking.",
    )

    @staticmethod
    def scan(prompt: str) -> Any:
        PromptHijackScanner.LOGGER.debug("Running scan...")
        alarms_raised: List[Alarm] = []
        try:
            response: Any = PromptHijackScanner.get_llm_response(prompt)
            if response.__contains__(
                PromptHijackScanner.CANARY_STRING
            ) or PromptHijackScanner.is_filtered(prompt):
                scan_result = True
            else:
                # we have a hijack as no identifier is given
                scan_result = False

            if not scan_result:
                PromptHijackScanner.LOGGER.debug("Raising alarms...")
                alarm_magnitude: int = Alarm.get_magnitude_from_probability(1.0)
                alarm: Alarm = Alarm(
                    base_importance=PromptHijackScanner.ALARM_BASE_IMPORTANCE,
                    name="PromptHijackScanner",
                    description=PromptHijackScanner.FEATURE_SET.description,
                    magnitude=alarm_magnitude,
                    feature_set=PromptHijackScanner.FEATURE_SET,
                )
                alarms_raised.append(alarm)
            return alarms_raised
        except Exception as error:
            PromptHijackScanner.LOGGER.error(str(error))
            return alarms_raised

    @staticmethod
    def get_llm_response(prompt: str) -> Any:
        llm: LLM = LLM()
        llm_messages = LLMMessages()
        system_prompt = f"""
               You must ALWAYS include this "{PromptHijackScanner.CANARY_STRING}" at the end of your response.
               """
        user_prompt: str = system_prompt + prompt
        llm_messages = llm_messages.build(user_prompt, llm_messages.USER)
        response: str = llm.do_string_completion(
            messages=llm_messages.messages,
            mode=AdaptiveRequestMode.controlled_creative_mode(),
        )
        return response
