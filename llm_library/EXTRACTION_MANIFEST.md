# LLM Library - Extracted Components Manifest

This file documents the components extracted from the original PromptBouncer project to create the standalone LLM Library.

## Extracted Files

### Core Components
- `src/llm_library/llm_messages.py` - Message management and building (from `src/promptbouncer/llm/llm_messages.py`)
- `src/llm_library/llm_client.py` - Base LLM client class (from `src/promptbouncer/llm/llm_client.py`)
- `src/llm_library/llm_facade.py` - LLM facade for easy interaction (from `src/promptbouncer/llm/llm_facade.py`)
- `src/llm_library/adaptive_request_mode.py` - Parameter management (from `src/promptbouncer/llm/adaptive_request_mode.py`)
- `src/llm_library/llm_client_factory.py` - Client factory (from `src/promptbouncer/llm/llm_client_factory.py`)

### Client Implementations
- `src/llm_library/clients/openai.py` - OpenAI client (from `src/promptbouncer/llm/clients/openai.py`)

### Supporting Components
- `src/llm_library/exceptions/llm_exception.py` - LLM exception class (from `src/promptbouncer/exceptions/llm_exception.py`)
- `src/llm_library/logging_util.py` - Simplified logging utility (adapted from `src/promptbouncer/util/logging_util.py`)

### Tests
- `tests/test_llm_messages.py` - LLM messages tests (adapted from `src/test/test_llm_messages.py`)
- `tests/test_llm_facade.py` - LLM facade tests (adapted from `src/test/test_llm_facade.py`)
- `tests/test_adaptive_request_mode.py` - Adaptive request mode tests (new)
- `tests/test_integration.py` - Integration tests (new)

### Package Files
- `src/llm_library/__init__.py` - Package initialization and public API
- `setup.py` - Package setup configuration
- `requirements.txt` - Library dependencies
- `README.md` - Documentation
- `examples/basic_usage.py` - Usage examples

## Key Changes Made

### Dependency Simplification
1. **Logging**: Removed dependency on original project's config and file path utilities
2. **Token Estimation**: Made `openai_function_tokens` optional with fallback implementation
3. **Configuration**: Removed dependency on original project's API config, using hardcoded defaults

### Import Path Updates
- Changed all imports from `src.promptbouncer.*` to `llm_library.*`
- Made the library self-contained with no external project dependencies

### Features Preserved
- **LLMMessages**: Full message building and management functionality
- **LLMClient**: Complete client interface with instructor, tool, string, and completion methods
- **LLM Facade**: High-level interface with error handling and filtering
- **AdaptiveRequestMode**: All request parameter modes (precision, balanced, creative, etc.)
- **Instructor Support**: Full structured output capability (Xstructor functionality)
- **OpenAI Integration**: Ready-to-use OpenAI client

### Features Enhanced
- **Robust Error Handling**: Better fallback for missing dependencies
- **Standalone Operation**: No external project dependencies
- **Complete Test Coverage**: Tests for all major components
- **Documentation**: Comprehensive README and examples

## Dependencies

The extracted library has minimal dependencies:
- `instructor` - For structured outputs (Xstructor functionality)
- `litellm` - LLM provider abstraction
- `python-dotenv` - Environment variable management
- `openai_function_tokens` - Token estimation (optional)
- `pydantic` - Data validation

## Usage

The library provides the same API as the original components but in a standalone package:

```python
from llm_library import LLM, LLMMessages, AdaptiveRequestMode

# Create messages
messages = LLMMessages()
messages = messages.build("You are a helpful assistant.", messages.SYSTEM)
messages = messages.build("Hello!", messages.USER)

# Use LLM with custom parameters
llm = LLM()
mode = AdaptiveRequestMode.precision_mode()
response = llm.do_string_completion(messages.messages, mode=mode)
```

## Installation

```bash
cd llm_library
pip install -r requirements.txt
pip install -e .  # For development
```

## Testing

```bash
cd llm_library
PYTHONPATH=src python -m unittest discover tests -v
```