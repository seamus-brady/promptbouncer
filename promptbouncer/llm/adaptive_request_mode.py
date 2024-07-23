#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from __future__ import annotations

from enum import StrEnum
from typing import Optional


class AdaptiveRequestMode:
    """A class to manage and adapt various parameters for LLMs."""

    class Mode(StrEnum):
        #  Low Temperature with Low Top_p
        PRECISION_MODE = "Precision Mode"

        # Low Temperature with High Top_p
        CONTROLLED_CREATIVE_MODE = "Controlled Creative Mode"

        # High Temperature with Low Top_p
        DYNAMIC_FOCUSED_MODE = "Dynamic Focused Mode"

        # High Temperature with High Top_p
        EXPLORATORY_MODE = "Exploratory Mode"

        # moderate temperature and top_p settings
        BALANCED_MODE = "Balanced Mode"

    DEFAULT_TEMPERATURE: Optional[float] = 0.5
    DEFAULT_TOP_P: Optional[float] = 0.5
    DEFAULT_MAX_TOKENS: Optional[int] = 4096

    # not in use currently
    DEFAULT_STOP: Optional[str] = None
    DEFAULT_PRESENCE_PENALTY: Optional[float] = 0
    DEFAULT_FREQUENCY_PENALTY: Optional[float] = 0

    def __init__(self, mode: AdaptiveRequestMode.Mode = None) -> None:
        self._mode: AdaptiveRequestMode.Mode = mode
        if self.mode is not None:
            self.init_mode()
        else:
            # set defaults
            self._mode = AdaptiveRequestMode.Mode.BALANCED_MODE
            self._temperature: float = self.DEFAULT_TEMPERATURE
            self._top_p: float = self.DEFAULT_TOP_P
            self._max_tokens: int = self.DEFAULT_MAX_TOKENS

    @staticmethod
    def instance() -> AdaptiveRequestMode:
        return AdaptiveRequestMode()

    @staticmethod
    def precision_mode() -> AdaptiveRequestMode:
        return AdaptiveRequestMode(mode=AdaptiveRequestMode.Mode.PRECISION_MODE)

    @staticmethod
    def controlled_creative_mode() -> AdaptiveRequestMode:
        return AdaptiveRequestMode(
            mode=AdaptiveRequestMode.Mode.CONTROLLED_CREATIVE_MODE
        )

    @staticmethod
    def dynamic_focused_mode() -> AdaptiveRequestMode:
        return AdaptiveRequestMode(mode=AdaptiveRequestMode.Mode.DYNAMIC_FOCUSED_MODE)

    @staticmethod
    def exploratory_mode() -> AdaptiveRequestMode:
        return AdaptiveRequestMode(mode=AdaptiveRequestMode.Mode.EXPLORATORY_MODE)

    @staticmethod
    def balanced_mode() -> AdaptiveRequestMode:
        return AdaptiveRequestMode(mode=AdaptiveRequestMode.Mode.BALANCED_MODE)

    @property
    def mode(self) -> AdaptiveRequestMode.Mode:
        return self._mode

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def top_p(self) -> float:
        return self._top_p

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    def init_mode(self) -> None:
        if self.mode is not None:
            #  Low Temperature with Low Top_p
            if self.mode == AdaptiveRequestMode.Mode.PRECISION_MODE:
                self._temperature = 0.2  # type: ignore[no-redef]
                self._top_p = 0.1  # type: ignore[no-redef]
                self._max_tokens = self.DEFAULT_MAX_TOKENS  # type: ignore[no-redef]

            # Low Temperature with High Top_p
            if self.mode == AdaptiveRequestMode.Mode.CONTROLLED_CREATIVE_MODE:
                self._temperature: float = 0.2  # type: ignore[no-redef]
                self._top_p: float = 0.9  # type: ignore[no-redef]
                self._max_tokens: int = self.DEFAULT_MAX_TOKENS  # type: ignore[no-redef]

            # High Temperature with Low Top_p
            if self.mode == AdaptiveRequestMode.Mode.DYNAMIC_FOCUSED_MODE:
                self._temperature: float = 0.9  # type: ignore[no-redef]
                self._top_p: float = 0.2  # type: ignore[no-redef]
                self._max_tokens: int = self.DEFAULT_MAX_TOKENS  # type: ignore[no-redef]

            # High Temperature with High Top_p
            if self.mode == AdaptiveRequestMode.Mode.EXPLORATORY_MODE:
                self._temperature: float = 0.9  # type: ignore[no-redef]
                self._top_p: float = 0.9  # type: ignore[no-redef]
                self._max_tokens: int = self.DEFAULT_MAX_TOKENS  # type: ignore[no-redef]

            # moderate temperature and top_p settings
            if self.mode == AdaptiveRequestMode.Mode.BALANCED_MODE:
                self._temperature: float = 0.5  # type: ignore[no-redef]
                self._top_p: float = 0.5  # type: ignore[no-redef]
                self._max_tokens: int = self.DEFAULT_MAX_TOKENS  # type: ignore[no-redef]
