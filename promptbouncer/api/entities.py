#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import List, Optional
from pydantic import BaseModel


class ThreatScanner(BaseModel):
    """Represents one type of scanner that looks for a specific threat."""
    name: str
    importance: int
    magnitude: int


class ThreatAssessmentRequest(BaseModel):
    """A request to do a threat assessment."""
    threat_scanners: Optional[List[ThreatScanner]] = []
    prompt: str


class Threat(BaseModel):
    """A threat that was found during a threat assessment."""
    name: str
    importance: int
    magnitude: int


class ThreatAssessmentResponse(BaseModel):
    """A response to a request for a threat assessment."""
    threats: Optional[List[Threat]] = []
    assessment_score: float
    assessment_description: str
