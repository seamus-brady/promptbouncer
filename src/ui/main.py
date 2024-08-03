#  Copyright (c) 2024. Prediction By Invention https://predictionbyinvention.com/
#
#  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

###########################################################################################
# Basic UI for Prompt Bouncer API demo
###########################################################################################

import os
import sys
import time
from pathlib import Path
from typing import List

# add parent path to sys.path
sys.path.insert(0, Path(__file__).parent.__str__())
sys.path.insert(0, Path(__file__).parent.parent.__str__())
sys.path.insert(0, Path(__file__).parent.parent.parent.__str__())

from src.promptbouncer.api.bouncer import Bouncer
from src.promptbouncer.api.entities import ThreatAssessment

import streamlit as st


###########################################################################################
# Functions for UI
###########################################################################################

def get_absolute_image_path(relative_image_path):
    """Get logo path."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_image_path = os.path.join(script_dir, relative_image_path)
    return absolute_image_path


def generate_html_table(data: List[dict], width: str = "100%") -> str:
    """Create a function to generate HTML table."""
    html = f'<table style="width:{width}; border-collapse: collapse;">'
    html += '<thead><tr>'
    # Adding headers
    for header in data[0].keys():
        html += f'<th style="border: 1px solid black; padding: 8px; text-align: left;">{header}</th>'
    html += '</tr></thead>'
    html += '<tbody>'
    # Adding rows
    for row in data:
        html += '<tr>'
        for value in row.values():
            html += f'<td style="border: 1px solid black; padding: 8px; text-align: left;">{value}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html


def do_threat_assessment():
    """Main function to call Prompt Bouncer"""
    try:
        threat_assessment: ThreatAssessment = Bouncer.door_check(prompt)
        st.title("The Bouncer's Threat Assessment Report")

        st.header("Assessment Summary")

        # Convert assessment summary to a list of dictionaries
        assessment_data = [
            {"Metric": "Assessment Score", "Value": threat_assessment.assessment_score},
            {"Metric": "Assessment Description", "Value": threat_assessment.assessment_description},
            {"Metric": "Assessment Confidence", "Value": threat_assessment.assessment_confidence},
            {"Metric": "Recommendation", "Value": threat_assessment.recommendation},
            {"Metric": "Time Taken in Seconds", "Value": threat_assessment.time_taken_seconds}
        ]

        # Display the assessment summary as an HTML table
        st.markdown(generate_html_table(assessment_data, "80%"), unsafe_allow_html=True)

        if len(threat_assessment.threats) == 0:
            st.header("No threats found!")
        else:
            st.header("Threats Details")
            # Convert threats to a list of dictionaries
            threats_data = [
                {
                    "Threat Scan": threat.threat_scan,
                    "Description": threat.threat_scan_description,
                    "Threat Level": threat.threat_level,
                    "Threat Details": threat.threat_details,
                    "Confidence": threat.confidence
                }
                for threat in threat_assessment.threats
            ]

            # Display the assessment summary as an HTML table
            st.markdown(generate_html_table(threats_data), unsafe_allow_html=True)

    except:  # noqa
        st.write("There was an error doing the threat assessment! Please try again.")


def count_words(text):
    """Function to count words"""
    try:
        words = text.split()
        return len(words)
    except:  # noqa
        raise ValueError("Error counting max words!")


def is_rate_limited():
    """Function to check rate limit."""
    try:
        current_time = time.time()
        if current_time - st.session_state['last_action_time'] < RATE_LIMIT_SECONDS:
            return True
        else:
            st.session_state['last_action_time'] = current_time
            return False
    except:  # noqa
        raise ValueError("Error in rate limiting!")

###########################################################################################
# App config
###########################################################################################

# Arbitrary maximum text length
MAX_WORD_COUNT = 1000

# Define rate limit parameters, allow one action per 10 seconds
RATE_LIMIT_SECONDS = 10

# logo path
relative_path_logo = "promptbouncer-logo-smaller.png"
absolute_path_logo = get_absolute_image_path(relative_path_logo)

# favicon path
relative_path_icon = "favicon.ico"
relative_path_icon = get_absolute_image_path(relative_path_icon)


# Set the page configuration, including the page title
st.set_page_config(
    page_title="Prompt Bouncer - Threat Assessment API Playground",
    page_icon=relative_path_icon,
    layout="wide"
)


###########################################################################################
# Main page layout
###########################################################################################

st.title("Prompt Bouncer")

# Create columns
col1, col2, col3 = st.columns([1, 3, 1])

# Display logo in the first column
with col1:
    st.image(absolute_path_logo)

# Display text in the second column
with col2:
    st.write("## Threat Assessment API Playground")
    st.markdown(""" 
    - Enter a prompt below, click Submit and the Bouncer will give a threat assessment.
    - For more details on how to use on Prompt Bouncer, please see the [main website](https://promptbouncer.com).
    """)

st.markdown("<hr>", unsafe_allow_html=True)

# Input field for the user to enter the prompt
prompt = st.text_area("Enter your prompt:")

# Initialize session state
if 'last_action_time' not in st.session_state:
    st.session_state['last_action_time'] = 0

# Button to submit the prompt
if st.button("Submit"):
    if prompt:
        if is_rate_limited():
            st.warning(f"Rate limit exceeded. Please wait {RATE_LIMIT_SECONDS} seconds before trying again.")
        else:
            # Check the length of the input text
            word_count = count_words(prompt)
            if word_count > MAX_WORD_COUNT:
                st.warning(f"""
                Text exceeds the maximum length of {MAX_WORD_COUNT} words for the UI. Please shorten your prompt.
                """)
            else:
                with st.spinner('The Bouncer is assessing the prompt...'):
                    do_threat_assessment()
    else:
        st.write("Please enter a prompt.")

st.markdown("<hr>", unsafe_allow_html=True)
st.header("Disclaimer and Terms of Use")
st.write("""
- This service is from demonstration purposes only. 
- The API has a rate limit of one query every 10 seconds.
- No prompts are stored, logged or used for training AI.
    
THIS SERVICE IS PROVIDED "AS IS" WITHOUT ANY WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. THE AUTHORS OR COPYRIGHT HOLDERS SHALL NOT BE LIABLE FOR ANY CLAIMS, DAMAGES, OR OTHER LIABILITIES, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SERVICE OR THE USE OF, OR OTHER DEALINGS WITH, THE SERVICE.
""")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© 2024 Prediction By Invention")