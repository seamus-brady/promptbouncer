#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from promptbouncer.exceptions.llm_exception import LLMException

#
#
#
#
from promptbouncer.llm.clients.openai import OpenAIClient
from promptbouncer.llm.llm_client import LLMClient


class LLMClientFactory:
    """
    Instantiates the correct LLMClient.
    """

    @staticmethod
    def llm_client() -> LLMClient:
        try:
            return OpenAIClient()
        except Exception as error:
            raise LLMException(str(error))
