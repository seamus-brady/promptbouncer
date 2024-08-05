
# Technical Overview of Prompt Bouncer Classes

## Overall Workflow

1. **Incoming Prompt**: A prompt is received for assessment.
2. **ThreatScan**: The `ThreatScan` class runs multiple scanners on the prompt to detect any threats.
3. **Alarms**: Each scanner returns alarms if threats are detected.
4. **Bouncer**: The `Bouncer` class processes these alarms to calculate an overall threat level, confidence, and recommendation.
5. **Threat Assessment**: A detailed `ThreatAssessment` is generated and returned, including the list of detected threats, the overall threat level, confidence, and recommendation on how to handle the prompt.

This setup provides a robust framework for assessing threats in text prompts using a combination of different scanning techniques and a central processing mechanism to aggregate and interpret the results.

## `entities.py`

This file defines several classes using Pydantic, which is a library for data validation and settings management using Python type annotations.

- **`ThreatScanner`**: Represents a scanner that looks for a specific threat.
- **`ThreatAssessmentRequest`**: Represents a request to do a threat assessment.
- **`Threat`**: Represents a threat found during a threat assessment, including details like the scanner name, threat level, and confidence.
- **`ThreatAssessment`**: Represents the response to a threat assessment request, including a list of threats, an assessment score, a description, confidence level, a recommendation, and the time taken to perform the assessment.

## `bouncer.py`

This file defines the `Bouncer` class, which provides a security service for assessing threats in prompts.

- **`Bouncer` Class**:
  - Contains an inner `Recommendation` class that defines possible recommendations for a prompt (e.g., let through, inspect threats, stop entry).
  - **`do_threat_assessment` Method**:
    - Takes an incoming prompt and assesses it for threats.
    - Runs various threat scanners, collects alarms, and processes them to determine an overall threat level, description, confidence, and recommendation.
    - Returns a `ThreatAssessment` object with the results.
  - **`get_recommendation` Method**: Determines the recommendation based on the threat level.

## `alarm.py`

This file defines the `Alarm` class, which represents alarms in the system, and contains several static methods for processing alarms.

- **`Alarm` Class**:
  - Contains constants for different threat levels (moderate, serious, critical) and their weights.
  - **`get_threat_level_string` Method**: Converts a threat level integer to a string.
  - **`calculate_threat_level` Method**: Calculates a weighted threat level based on the number of moderate, serious, and critical alarms.
  - **`calculate_overall_confidence` Method**: Calculates a weighted average confidence level of all alarms.
  - **`count_threat_levels` Method**: Counts the number of alarms at each threat level.
  - **`get_threat_description` Method**: Provides a human-readable description of the threat level.

## `threat_scan.py`

This file defines the `ThreatScan` class, which manages running a set of threat scanners on incoming prompts.

- **`run_text_scanner` Function**: Runs a given scanner on a prompt.
- **`ThreatScan` Class**:
  - Initializes with a dictionary of various threat scanners.
  - **`instance` Method**: Returns an instance of `ThreatScan`.
  - **`is_filtered` Method**: Checks if the prompt is filtered out by the language model.
  - **`run` Method**: Runs all the scanners on the incoming prompt using a thread pool, collects the results, and returns a list of alarms.
  - **`get_threadpool` Method**: Returns a thread pool executor with a maximum number of worker threads.
  - **`add_filter_alarm` Method**: Creates an alarm if the prompt is filtered by the language model.


