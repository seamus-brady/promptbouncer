# LLM Library

A standalone Python library for managing Large Language Model interactions, extracted from the PromptBouncer project.

## Features

- **LLMMessages**: Message management and building with role-based structure
- **LLMClient**: Base client for LLM providers with support for multiple completion types
- **LLM Facade**: High-level interface for easy LLM interaction
- **AdaptiveRequestMode**: Parameter management for different LLM request strategies
- **Instructor Support**: Structured outputs using the instructor library (Xstructor)
- **OpenAI Integration**: Ready-to-use OpenAI client implementation

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from llm_library import LLM, LLMMessages, AdaptiveRequestMode

# Create messages
messages = LLMMessages()
messages = messages.build("You are a helpful assistant.", messages.SYSTEM)
messages = messages.build("What is Python?", messages.USER)

# Initialize LLM facade
llm = LLM()

# Simple completion
response = llm.do_string_completion(messages.messages)
print(response)

# With custom parameters
mode = AdaptiveRequestMode.precision_mode()
response = llm.do_completion(messages.messages, mode=mode)
```

## Structured Outputs (Instructor)

```python
from pydantic import BaseModel
from llm_library import LLM, LLMMessages

class Response(BaseModel):
    answer: str
    confidence: float

messages = LLMMessages()
messages = messages.build("Extract the answer and confidence.", messages.SYSTEM)
messages = messages.build("The sky is blue.", messages.USER)

llm = LLM()
structured_response = llm.do_instructor(messages.messages, Response)
print(structured_response.answer)  # "The sky is blue"
print(structured_response.confidence)  # 0.95
```

## Request Modes

The library supports different request modes for various use cases:

- **Precision Mode**: Low temperature (0.2), low top_p (0.1) - for factual, deterministic responses
- **Controlled Creative Mode**: Low temperature (0.2), high top_p (0.9) - for creative but controlled responses
- **Dynamic Focused Mode**: High temperature (0.9), low top_p (0.2) - for varied but focused responses
- **Exploratory Mode**: High temperature (0.9), high top_p (0.9) - for highly creative responses
- **Balanced Mode**: Medium temperature (0.5), medium top_p (0.5) - default balanced approach

## Configuration

Set your OpenAI API key in environment variables:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```
OPENAI_API_KEY=your-api-key-here
```

## Testing

Run the tests:

```bash
python -m unittest discover tests
```

## Dependencies

- `instructor`: For structured outputs
- `litellm`: For LLM provider abstraction
- `python-dotenv`: For environment variable management
- `openai_function_tokens`: For token estimation (optional)
- `pydantic`: For data validation

## License

MIT License - see LICENSE file for details.

## Credits

Extracted from the PromptBouncer project by seamus@corvideon.ie