# Prompt Bouncer

A first line of defense against prompt-based attacks with real-time threat assessment.

![Prompt Bouncer Logo](doc/img/promptbouncer-logo-small.png)

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Available Scanners](#available-scanners)
- [Usage](#usage)
  - [As a Library](#as-a-library)
  - [As a REST Service](#as-a-rest-service)
  - [As a UI Service](#as-a-ui-service)
- [Installation](#installation)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

## Overview

Prompt Bouncer is a prototype tool that helps AI developers stop prompt-based attacks by providing a comprehensive threat assessment of any incoming prompt. Acting as security personnel at the door of your AI system, it checks every incoming prompt to ensure safety before allowing it through. The tool provides a clear Go/No-Go decision based on multiple security scans, helping protect your LLM applications from various threats.

## Key Features

- **Go/No-Go Decisions**: Quick, clear decisions on prompt safety
- **Multiple Integration Options**: Use as a library, REST service, or with UI
- **Comprehensive Scanning**: Multiple layers of security analysis
- **Flexible Deployment**: Easy integration into existing workflows
- **Real-time Analysis**: Immediate threat detection and response

## Available Scanners

Prompt Bouncer includes multiple specialized scanners for thorough threat detection:

| Scanner Type | Threat Level | Description |
|--------------|--------------|-------------|
| Prompt Injection | Critical | Detects direct/indirect injection, instruction injection, code injection |
| Prompt Leakage | Critical | Identifies potential prompt leakage using canary strings |
| Prompt Hijack | Critical | Detects goal hijacking attempts |
| Inappropriate Content | Serious | Scans for illegal activity, hate speech, malware, etc. |
| Code Detection | Moderate | Identifies potentially malicious code fragments |
| Language Detection | Moderate | Prevents hidden instructions in foreign languages |
| Perplexity | Moderate | Analyzes input complexity for hidden threats |
| Toxicity | Moderate | Detects toxic language and harmful content |
| Secrets | Moderate | Identifies sensitive information like API keys |

## Usage

### As a Library

```python
from promptbouncer import PromptBouncer

bouncer = PromptBouncer()
result = bouncer.validate_prompt("Your prompt here")
if result.is_safe:
    # Proceed with LLM call
```

### As a REST Service

Start the FastAPI server:

```bash
python -m invoke api
```

The API will be available at http://localhost:10001

### As a UI Service

Launch the Streamlit UI:

```bash
python -m invoke ui
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Prediction-by-Invention/promptbouncer.git
cd promptbouncer
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Development

The project uses several development tools:

```bash
# Run all checks
python -m invoke checks

# Run specific checks
python -m invoke test      # Run unit tests
python -m invoke mypy      # Type checking
python -m invoke formatter # Code formatting
python -m invoke linter    # Code linting
python -m invoke bandit    # Security checks
python -m invoke isort     # Import sorting
```

## Documentation

For more detailed information, please see:

- [Full Documentation](https://github.com/seamus-brady/promptbouncer/tree/main/doc)

## License

This project is licensed under the MIT License - see the [License.txt](License.txt) file for details.

## Disclaimer

This is a prototype tool and should be used with caution in production environments. Always perform thorough testing and validation for your specific use case.
