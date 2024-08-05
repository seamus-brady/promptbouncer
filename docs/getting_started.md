# Getting Started

## Introduction

This document provides a step-by-step guide to setting up the Prompt Bouncer project using the built-in `venv` module to create a virtual environment.

## Prerequisites

- Ensure you have Python 3.8 or later installed on your system. Python 3.11 is recommended. You can download the latest version from the [official Python website](https://www.python.org/).

## Steps to Set Up the Prompt Bouncer Project Using `venv`

### Step 1: Clone the Repository

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to clone the project.
3. Clone the Prompt Bouncer repository:

   ```sh
   git clone https://github.com/Prediction-by-Invention/promptbouncer.git
   cd promptbouncer
   ```

### Step 2: Create a Virtual Environment

1. Inside the project directory, create a virtual environment using the `venv` module:

   ```sh
   python3 -m venv venv
   ```

   This command creates a directory named `venv` containing the virtual environment.

### Step 3: Activate the Virtual Environment

- **Windows:**

  ```sh
  venv\Scripts\activate
  ```

- **macOS and Linux:**

  ```sh
  source venv/bin/activate
  ```

  After activation, your terminal prompt will change to indicate that you are now working inside the virtual environment.

### Step 4: Install Project Dependencies

1. With the virtual environment activated, install the necessary packages using `pip`:

   ```sh
   pip install -r requirements.txt
   ```

### Step 5: Deactivate the Virtual Environment

1. Once you are done working in your virtual environment, deactivate it:

   ```sh
   deactivate
   ```

### Step 6: Reactivate the Virtual Environment

1. Whenever you return to your project, reactivate the virtual environment:

- **Windows:**

  ```sh
  venv\Scripts\activate
  ```

- **macOS and Linux:**

  ```sh
  source venv/bin/activate
  ```

### Step 7: Install Dependencies from `requirements.txt`

1. If you are setting up the project on a new machine or after cloning from a repository, activate the virtual environment and install dependencies from the `requirements.txt` file:

   ```sh
   pip install -r requirements.txt
   ```

## Conclusion

By following these steps, you can set up the Prompt Bouncer project using `venv`, manage your dependencies, and ensure a clean and isolated development environment.
