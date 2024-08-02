#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import sys
import time
from pathlib import Path

import pandas as pd

# add parent path to sys.path
sys.path.insert(0, Path(__file__).parent.__str__())
sys.path.insert(0, Path(__file__).parent.parent.__str__())
sys.path.insert(0, Path(__file__).parent.parent.parent.__str__())

from src.promptbouncer.api.bouncer import Bouncer
from src.promptbouncer.api.entities import ThreatAssessment

import streamlit as st

# Set up the Streamlit app
st.title("Prompt Bouncer: Threat Assessment API")

# Input field for the user to enter the prompt
prompt = st.text_input("Enter your prompt:")


def timed_function_call(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time


def do_threat_assessment():
    threat_assessment: ThreatAssessment = Bouncer.door_check(prompt)
    st.header("Threats Details")
    # Convert threats to a DataFrame
    threats_data = {
        "Threat Scan": [threat.threat_scan for threat in threat_assessment.threats],
        "Description": [threat.threat_scan_description for threat in threat_assessment.threats],
        "Threat Level": [threat.threat_level for threat in threat_assessment.threats],
        "Threat Details": [threat.threat_details for threat in threat_assessment.threats],
        "Confidence": [threat.confidence for threat in threat_assessment.threats]
    }
    df_threats = pd.DataFrame(threats_data)
    # Display the DataFrame as a table in Streamlit
    st.table(df_threats)
    return "Function complete"

# Button to submit the prompt
if st.button("Submit"):
    if prompt:
        result, elapsed_time = timed_function_call(do_threat_assessment, 2)
        print(f"Result: {result}")
        print(f"Elapsed Time: {elapsed_time} seconds")
        do_threat_assessment()
    else:
        st.write("Please enter a prompt.")
