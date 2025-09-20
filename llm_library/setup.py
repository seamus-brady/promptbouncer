#!/usr/bin/env python
"""Setup script for the LLM Library package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="llm-library",
    version="1.0.0",
    author="seamus@corvideon.ie",
    description="A standalone library for managing Large Language Model interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seamus-brady/promptbouncer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest", "black", "isort", "mypy", "flake8"],
        "test": ["pytest", "pytest-cov"],
    },
    project_urls={
        "Bug Reports": "https://github.com/seamus-brady/promptbouncer/issues",
        "Source": "https://github.com/seamus-brady/promptbouncer",
    },
)