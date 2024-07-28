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
import os

from dotenv import load_dotenv

from src.promptbouncer.config.api import DEFAULT_OPENAI_MODEL
from src.promptbouncer.llm.llm_client import LLMClient
from src.promptbouncer.util.logging_util import LoggingUtil

# take environment variables from .env.
load_dotenv()

# OpenAI public api
OPENI_API_KEY = os.environ["OPENAI_API_KEY"]


class OpenAIClient(LLMClient):
    """An interface to the OpenAI API. Used only from within the LLM facade parent class."""

    LOGGER = LoggingUtil.instance("<OpenAIClient>")

    def __init__(self) -> None:
        super().__init__()
        OpenAIClient.LOGGER.info("Initializing OpenAIClient...")
        self._model = DEFAULT_OPENAI_MODEL
