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
#
#
from typing import Any, List

from src.promptbouncer.api.alarm import Alarm
from src.promptbouncer.llm.adaptive_request_mode import AdaptiveRequestMode
from src.promptbouncer.llm.llm_facade import LLM
from src.promptbouncer.llm.llm_messages import LLMMessages
from src.promptbouncer.scanners.abstract_scanner import AbstractThreatScanner
from src.promptbouncer.util.logging_util import LoggingUtil


class PromptHijackScanner(AbstractThreatScanner):
    """
    A class to check prompt hijacking. If the response does not contain the canary,
    this may indicate goal hijacking prompt injection
    Based on https://vigil.deadbits.ai/overview/use-vigil/scanners/canary-tokens
    """

    LOGGER = LoggingUtil.instance("<PromptHijackScanner>")

    THREAT_SCANNER_NAME = "PromptHijackScanner"
    THREAT_SCANNER_DESC = "A scan to check prompt hijacking."
    THREAT_LEVEL = Alarm.THREAT_CRITICAL

    CANARY_STRING: str = "3fabe23c5d8e9a7b"

    @staticmethod
    def scan(prompt: str) -> Any:
        PromptHijackScanner.LOGGER.debug("Running scan...")
        alarms_raised: List[Alarm] = []
        try:
            response: Any = PromptHijackScanner.get_llm_response(prompt)
            if response.__contains__(
                PromptHijackScanner.CANARY_STRING
            ) or PromptHijackScanner.is_filtered(prompt):
                scan_result_innocuous = True
            else:
                # we have a hijack as no identifier is given
                scan_result_innocuous = False

            if not scan_result_innocuous:
                PromptHijackScanner.LOGGER.debug("Raising alarms...")
                alarm: Alarm = Alarm(
                    threat_level=PromptHijackScanner.THREAT_LEVEL,
                    threat_details="""
                    This prompt failed to return the canary string. It may be a prompt hijack attempt.
                    """.strip(),
                    threat_scanner_name=PromptHijackScanner.THREAT_SCANNER_NAME,
                    threat_scanner_description=PromptHijackScanner.THREAT_SCANNER_DESC,
                    # confidence in this scanner is always 100% as the test is binary
                    confidence=1.0,
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
