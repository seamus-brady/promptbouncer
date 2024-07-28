#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import uvicorn
import yaml  # noqa
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from src.promptbouncer.api.bouncer import Bouncer
from src.promptbouncer.api.entities import ThreatAssessment, ThreatAssessmentRequest
from src.promptbouncer.exceptions.api_exception import APIException
from src.promptbouncer.util.file_path_util import FilePathUtil
from src.promptbouncer.util.logging_util import LoggingUtil

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


@app.post("/v1/threat-assessment", response_model=ThreatAssessment)
def do_threat_assessment(request: ThreatAssessmentRequest):
    LoggingUtil.instance("<MAIN>").debug("ThreatScan running...")
    try:
        incoming_prompt: str = request.prompt
        return Bouncer.door_check(incoming_prompt)
    except Exception as error:
        LoggingUtil.instance("<MAIN>").error(error.__str__())
        raise APIException(error.__str__())


if __name__ == "__main__":
    uvicorn.run(app, port=10001)
