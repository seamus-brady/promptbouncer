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

import re
from typing import Any, List

from promptbouncer.alarms.alarm import Alarm
from promptbouncer.scanners.abstract_scanner import AbstractThreatScanner
from promptbouncer.util.logging_util import LoggingUtil


class CodeScanner(AbstractThreatScanner):
    """
    Scans for any code fragments in a prompt.
    The scanner is currently limited to extracting and detecting code snippets in JavaScript & Python.
    """

    LOGGER = LoggingUtil.instance("<CodeScanner>")

    THREAT_SCANNER_NAME = "CodeScanner"
    THREAT_SCANNER_DESC = "This scan looks for code in a prompt that may be a security threat.",
    THREAT_LEVEL = Alarm.THREAT_MODERATE

    @staticmethod
    def scan(prompt: str) -> Any:
        CodeScanner.LOGGER.debug("Running scan...")
        alarms_raised: List[Alarm] = []
        try:
            code_found: bool = CodeScanner.code_scan(prompt)
            if code_found:
                CodeScanner.LOGGER.debug("Raising alarms...")
                alarm: Alarm = Alarm(
                    threat_level=CodeScanner.THREAT_LEVEL,
                    threat_details="Code detected in prompt.",
                    threat_scanner_name=CodeScanner.THREAT_SCANNER_NAME,
                    threat_scanner_description=CodeScanner.THREAT_SCANNER_NAME,
                )
                alarms_raised.append(alarm)
            return alarms_raised
        except Exception as error:
            CodeScanner.LOGGER.error(str(error))
            return alarms_raised

    @staticmethod
    def code_scan(input_string: str) -> bool:
        try:
            if CodeScanner.detect_code_regex(input_string):  # type: ignore
                return True
            return False  # type: ignore
        except:  # noqa
            return False  # type: ignore

    @staticmethod
    def detect_code_regex(input_string: str):
        code_detected: bool = False
        # patterns that might indicate Python or JavaScript code
        python_patterns = [
            r"\bdef\b",  # Python function definition
            r"\bimport\b",  # Python import statement
            r"from\s+\w+\s+import",  # Python from import
            r"if\s+__name__\s*==\s*['__\"]__main__['__\"]:",  # Common Python main check
        ]

        javascript_patterns = [
            r"\bfunction\b",  # JavaScript function keyword
            r"\bvar\b",  # JavaScript var keyword
            r"\bconsole\.log\b",  # JavaScript console.log
            r"\bdocument\.getElementById\b",  # Common DOM method in JavaScript
        ]

        # check for Python patterns
        if any(re.search(pattern, input_string) for pattern in python_patterns):
            code_detected = True

        # check for JavaScript patterns
        if any(re.search(pattern, input_string) for pattern in javascript_patterns):
            code_detected = True

        return code_detected
