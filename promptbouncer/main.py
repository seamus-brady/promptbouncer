#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from typing import List, Dict

import uvicorn
import yaml  # noqa
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from promptbouncer.alarms.alarm import Alarm
from promptbouncer.api.entities import (
    Threat,
    ThreatAssessmentRequest,
    ThreatAssessmentResponse,
)
from promptbouncer.api.threat_scan import ThreatScan
from promptbouncer.exceptions.api_exception import APIException
from promptbouncer.util.file_path_util import FilePathUtil
from promptbouncer.util.logging_util import LoggingUtil

app = FastAPI()


def load_openapi():
    """Load the Prompt Bouncer OpenAPI spec from a YAML file."""
    if app.openapi_schema:
        return app.openapi_schema
    with open(FilePathUtil.api_spec_path(), "r") as file:
        try:
            openapi_schema = yaml.safe_load(file)
            app.openapi_schema = openapi_schema
            return app.openapi_schema
        except Exception as error:
            raise APIException(message=error.__str__())


# load the API spec
app.openapi = load_openapi  # type: ignore


@app.get("/")
def get_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Prompt Bouncer API</title>
    </head>
    <body>
        <h1>Welcome to the Prompt Bouncer API</h1>
        <p><a href="/docs">Go to API Documentation</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/v1/threat-assessment", response_model=ThreatAssessmentResponse)
def do_threat_assessment(request: ThreatAssessmentRequest):
    LoggingUtil.instance("<MAIN>").debug("ThreatScan running...")
    try:
        incoming_prompt: str = request.prompt
        alarms: List[Alarm] = ThreatScan.instance().run(incoming_prompt)
        threats: List[Threat] = []
        for alarm in alarms:
            threats.append(
                Threat(
                    threat_scan=alarm.threat_scanner_name,
                    threat_scan_description=alarm.threat_scanner_description,
                    threat_level=Alarm.get_threat_level_string(alarm.threat_level),
                    threat_details=alarm.threat_details
                )
            )

        threat_level_count_dict: Dict[int, int] = Alarm.count_threat_levels(alarms=alarms)

        assessment_score = Alarm.calculate_threat_level(
            threat_level_count_dict[Alarm.THREAT_MODERATE],
            threat_level_count_dict[Alarm.THREAT_SERIOUS],
            threat_level_count_dict[Alarm.THREAT_CRITICAL],
        ).__round__(2)

        # TODO: This should be calculated based on the input request
        assessment_description = "High risk due to multiple severe threats."
        return ThreatAssessmentResponse(
            threats=threats,
            assessment_score=assessment_score,
            assessment_description=assessment_description,
        )
    except Exception as error:
        LoggingUtil.instance("<MAIN>").error(error.__str__())
        raise APIException(error.__str__())


if __name__ == "__main__":
    uvicorn.run(app, port=10001)
