# Threat Assessment and Recommendation in Prompt Bouncer

## Table of Contents

- [Introduction](#introduction)
- [How Prompt Bouncer Comes Up with a Recommendation](#how-prompt-bouncer-comes-up-with-a-recommendation)
  - [Workflow](#workflow)
  - [Detailed Process](#detailed-process)
    - [Threat Scanning](#1-threat-scanning)
    - [Alarm Generation](#2-alarm-generation)
    - [Threat Assessment](#3-threat-assessment)
    - [Generating the Recommendation](#4-generating-the-recommendation)
- [Measurements for Threat Assessment](#measurements-for-threat-assessment)
  - [Weighted Threat Level](#weighted-threat-level)
  - [Overall Confidence](#overall-confidence)
  - [Using These Measurements to Assess a Threat](#using-these-measurements-to-assess-a-threat)

## Introduction

Prompt Bouncer is a security service designed to assess threats in incoming prompts and provide recommendations on how to handle them. This document outlines the process by which Prompt Bouncer comes up with a recommendation and describes how various measurements, such as weighted averages, are used to assess threats.

## How Prompt Bouncer Comes Up with a Recommendation

### Workflow

1. **Incoming Prompt**: A prompt is received for assessment.
2. **Threat Scanning**: The ThreatScan class runs multiple threat scanners on the prompt to detect any potential threats.
3. **Alarm Generation**: Each scanner generates alarms if threats are detected.
4. **Threat Assessment**: The Bouncer class processes these alarms to calculate an overall threat level, confidence, and generates a recommendation based on the results of all scanners.
5. **Recommendation**: Based on the calculated threat level, a recommendation is made on how to handle the prompt.

[Back to top](#table-of-contents)

### Detailed Process

#### 1. Threat Scanning

- The ThreatScan class initializes with a set of available threat scanners.
- Each scanner runs in parallel using a thread pool to quickly assess the incoming prompt.
- The results from each scanner are collected in the form of alarms.

#### 2. Alarm Generation

- Each alarm includes details such as the threat level, confidence score, and a description of the detected threat.
- Alarms are categorized based on their threat level (moderate, serious, critical).

#### 3. Threat Assessment

- The Bouncer class aggregates the alarms to calculate an overall threat level and confidence score.
- The following calculations are performed:
  - **Weighted Threat Level**: A weighted sum of all alarms is calculated to determine the overall threat level.
  - **Overall Confidence**: A weighted average of the confidence scores from all alarms is calculated.

#### 4. Generating the Recommendation

- Based on the overall threat level, the Bouncer class makes a recommendation using predefined thresholds:
  - **OK_LET_THROUGH**: Threat level ≤ 2
  - **INSPECT_THREATS**: Threat level > 2 and ≤ 6
  - **STOP_NO_ENTRY**: Threat level > 6 and ≤ 10

[Back to top](#table-of-contents)

## Measurements for Threat Assessment

### Weighted Threat Level

The weighted threat level is calculated as follows:

1. **Count Threat Levels**: Count the number of alarms at each threat level (moderate, serious, critical).
2. **Weighted Sum**: Calculate a weighted sum using predefined weights for each threat level.
   - Weights: Moderate = 1, Serious = 2, Critical = 3
3. **Normalization**: Normalize the weighted sum to a scale of 0-10 to get the overall threat level.

```python
@staticmethod
def calculate_threat_level(moderate: int, serious: int, critical: int) -> float:
    weights = Alarm.THREAT_WEIGHTS
    weighted_sum = (moderate * weights[1] + serious * weights[2] + critical * weights[3])
    total_alarms = moderate + serious + critical
    max_weighted_sum = total_alarms * weights[3]
    if max_weighted_sum == 0:
        return 0
    overall_threat_level = (weighted_sum / max_weighted_sum) * 10
    return overall_threat_level.__round__(2)
```

[Back to top](#table-of-contents)

### Overall Confidence

The overall confidence is calculated as follows:

1. **Sum of Confidence Scores**: Sum the confidence scores from all alarms.
2. **Weighted Average**: Calculate a weighted average of the confidence scores using the weights for each threat level.

```python
@staticmethod
def calculate_overall_confidence(alarms: List[Alarm]) -> float:
    if len(alarms) == 0:
        return 1.0
    total_weighted_score = 0.0
    total_weight = 0.0
    for alarm in alarms:
        weight = Alarm.THREAT_WEIGHTS[alarm.threat_level]
        total_weighted_score += weight * alarm.confidence
        total_weight += weight
    overall_confidence = total_weighted_score / total_weight
    return overall_confidence.__round__(2)
```

[Back to top](#table-of-contents)

### Using These Measurements to Assess a Threat

- **Threat Level**: Indicates the severity of the detected threats. Higher values suggest more serious threats.
- **Confidence Score**: Indicates the certainty of the detected threats. Higher values suggest greater confidence in the threat assessment.
- **Recommendation**: Provides actionable advice based on the threat level:
  - **OK_LET_THROUGH**: The prompt is safe to proceed.
  - **INSPECT_THREATS**: The prompt contains some threats and requires further inspection.
  - **STOP_NO_ENTRY**: The prompt contains serious threats and should not be allowed through.

By combining these measurements, Prompt Bouncer can provide a comprehensive assessment of the threats in an incoming prompt and recommend appropriate actions to mitigate potential risks.

[Back to top](#table-of-contents)