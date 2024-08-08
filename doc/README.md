# Prompt Bouncer Documentation

![Prompt Bouncer Logo](https://github.com/Prediction-by-Invention/promptbouncer/blob/main/doc/img/promptbouncer-logo-small.png)

# Table of Contents
- [Prompt Bouncer Documentation](#prompt-bouncer-documentation)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Steps to Install Prompt Bouncer from GitHub](#steps-to-install-prompt-bouncer-from-github)
    - [Clone the Repository](#clone-the-repository)
    - [Create a Virtual Environment](#create-a-virtual-environment)
    - [Install the Package](#install-the-package)
  - [REST API](#rest-api)
  - [Docker](#docker)
    - [Docker Build](#docker-build)
    - [Docker Run](#docker-run)
  - [Streamlit UI Playground](#streamlit-ui-playground)
  - [Technical Docs](#technical-docs)


## Requirements

- Prompt Bouncer should work with any version of Python. `3.8+` but `3.11` is recommended.
- Prompt Bouncer needs an Open AI key to operate. Internally the `GTP4-o` model is used as it is cheap and fast.
- Prompt Bouncer does not need a GPU and will work on most shared hosting environmentrs where Python is available, as well as on any cloud provider where Docker is available.

[Back to top](#table-of-contents)

## Setup

- You should create a `.env` in the root of your project and place your OpenAI API key in there.

```
# OpenAI API
OPENAI_API_KEY=sk-blahblahblah
```
- Prompt Bouncer will pick it up from here.
- Alternatively, set up the usual `OPENAI_API_KEY` environmental variable.

[Back to top](#table-of-contents)

## Steps to Install Prompt Bouncer from GitHub

### Clone the Repository:

First, clone the repository to your local machine using git.

```bash
git clone https://github.com/Prediction-by-Invention/promptbouncer.git
cd promptbouncer
```

### Create a Virtual Environment (Optional but recommended):

It's a good practice to create a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install the Package:

Use pip to install the package in editable mode. This allows you to make changes to the code and have those changes reflected immediately.

```bash
pip install -e .
```

[Back to top](#table-of-contents)


## REST API

- Prompt Bouncer comes with a FastAPI Swagger API.
- You can use the provided script below to start it:

```bash
bin/promptbouncer-fastapi
```

[Back to top](#table-of-contents)

## Docker

- Prompt Bouncer comes with a Docker build file.

### Docker Build

- You can use the provided script below to build the Docker image:

```bash
bin/docker-build
```

### Docker Run

- You can use the provided script below to run the Docker image :

```bash
bin/docker-run
```

[Back to top](#table-of-contents)

### Streamlit UI Playground

- Prompt Bouncer comes with a Streamlit UI Playground.
- You can use the provided script below to start it:

```bash
bin/promptbouncer-ui
```

[Back to top](#table-of-contents)

## Technical Docs

- [Technical Overview of Scans](technical_overview_scans.md)
- [Available Scanners in Prompt Bouncer](available_scanners.md)
- [Threat Assessment and Recommendation in Prompt Bouncer](threat_assessment_technical.md)
- [Handling Scenarios](handling_scenarios.md)

[Back to top](#table-of-contents)