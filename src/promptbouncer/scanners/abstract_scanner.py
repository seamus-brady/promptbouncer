#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
from abc import ABC
from typing import Any

from src.promptbouncer.llm.llm_facade import LLM


class AbstractThreatScanner(ABC):
    """Abstract parent class for all threat scanners."""

    @staticmethod
    def scan(prompt: str) -> Any:
        raise NotImplementedError

    @staticmethod
    def is_filtered(prompt: str) -> bool:
        """Checks to see if a message has been filtered by the LLM"""
        if prompt is not None and prompt.__contains__(LLM.ERROR_FILTERED):
            return True
        else:
            return False
