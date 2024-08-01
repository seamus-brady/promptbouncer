#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from fastapi.testclient import TestClient

from src.server.main import app

client = TestClient(app)


class TestApp(unittest.TestCase):
    client = TestClient(app)

    def test_root(self):
        response = client.get("/")
        self.assertTrue(response.status_code == 200)

    def test_threat_assessment(self):
        response = client.post("/v1/threat-assessment")
        self.assertTrue(response.status_code == 422)


if __name__ == "__main__":
    unittest.main()
