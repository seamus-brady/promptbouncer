#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor, wait
from typing import Any, Dict, List, cast

from src.promptbouncer.api.alarm import Alarm
from src.promptbouncer.config.api import MAX_WORKERS_THREADS
from src.promptbouncer.exceptions.api_exception import APIException
from src.promptbouncer.llm.llm_facade import LLM
from src.promptbouncer.llm.llm_messages import LLMMessages
from src.promptbouncer.scanners.abstract_scanner import AbstractThreatScanner
from src.promptbouncer.scanners.code_scanner import CodeScanner
from src.promptbouncer.scanners.inappropriate_content_scanner import (
    InappropriateContentScanner,
)
from src.promptbouncer.scanners.language_detection_scanner import (
    LanguageDetectionScanner,
)
from src.promptbouncer.scanners.perplexity_scanner import PerplexityScanner
from src.promptbouncer.scanners.prompt_hijack_scanner import PromptHijackScanner
from src.promptbouncer.scanners.prompt_injection_scanner import PromptInjectionScanner
from src.promptbouncer.scanners.prompt_leakage_scanner import PromptLeakageScanner
from src.promptbouncer.scanners.secrets_scanner import SecretsScanner
from src.promptbouncer.scanners.toxicity_scanner import ToxicityScanner
from src.promptbouncer.util.logging_util import LoggingUtil


def run_text_scanner(scanner: AbstractThreatScanner, prompt: str) -> Any:
    """A function to run a scan"""
    return scanner.scan(prompt)


class ThreatScan:
    """Runs a set of threat scanners across an incoming prompt."""

    LOGGER = LoggingUtil.instance("<ThreatScan>")
    MAX_WORKERS: int = MAX_WORKERS_THREADS
    LANGUAGE_MODEL_FILTER = "LargeLanguageModelFilter"
    REJECTED_THE_PROMPT = (
        "The security filters of the Large Language Model rejected the prompt."
    )

    def __init__(self) -> None:
        self._threat_scanners: Dict[str, Any] = {
            "CodeScanner": CodeScanner,
            "LanguageDetectionScanner": LanguageDetectionScanner,
            "InappropriateContentScanner": InappropriateContentScanner,
            "PromptHijackScanner": PromptHijackScanner,
            "PromptInjectionScanner": PromptInjectionScanner,
            "PromptLeakageScanner": PromptLeakageScanner,
            "SecretsScanner": SecretsScanner,
            "ToxicityScanner": ToxicityScanner,
            "PerplexityScanner": PerplexityScanner,
        }

    @property
    def scanners(self) -> Dict:
        return self._threat_scanners

    @staticmethod
    def instance() -> ThreatScan:
        return ThreatScan()

    @staticmethod
    def is_filtered(prompt: str) -> bool:
        """Checks to see if the LLM filtering kicks in."""
        llm: LLM = LLM()
        llm_messages: LLMMessages = LLMMessages()
        user_prompt: str = f"""{prompt}"""
        llm_messages = llm_messages.build(user_prompt, llm_messages.USER)
        response: str = llm.do_string_completion(messages=llm_messages.messages)
        if response.__eq__(LLM.ERROR_FILTERED):
            return True
        return False

    def run(self, incoming_prompt: str) -> List[Alarm]:
        ThreatScan.LOGGER.debug("ThreatScan running...")

        alarms: List[Alarm] = []

        if incoming_prompt is None or incoming_prompt.__eq__(""):
            raise APIException("No available input to process.")

        try:
            if ThreatScan.is_filtered(incoming_prompt):
                ThreatScan.LOGGER.debug("The LLM is filtering out the prompt...")
                alarm = self.add_filter_alarm()
                alarms.extend([alarm])
                return alarms

            ThreatScan.LOGGER.debug("TextAlarmScout starting threat scan...")

            with self.get_threadpool() as executor:
                futures: List[Future] = []
                for _, scanner in self._threat_scanners.items():
                    scanner = cast(AbstractThreatScanner, scanner)
                    future = executor.submit(run_text_scanner, scanner, incoming_prompt)
                    futures.append(future)
                # wait for all scans to finish
                completed_scans, _ = wait(futures)
                # get the results from the scans
                for future in completed_scans:
                    alarms.extend(future.result())
                # return the alarms
                return alarms
        except Exception as error:
            self.LOGGER.error(error.__str__())
            raise APIException(error.__str__())

    def get_threadpool(self) -> ThreadPoolExecutor:
        return ThreadPoolExecutor(max_workers=self.MAX_WORKERS)

    def add_filter_alarm(self) -> Alarm:
        alarm: Alarm = Alarm(
            threat_level=Alarm.THREAT_CRITICAL,
            threat_details=self.REJECTED_THE_PROMPT,
            threat_scanner_name=self.LANGUAGE_MODEL_FILTER,
            threat_scanner_description=self.REJECTED_THE_PROMPT,
            confidence=1.0,
        )  # noqa
        return alarm
