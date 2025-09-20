#!/usr/bin/env python
"""
Example usage of the LLM Library
"""
import os
from llm_library import LLM, LLMMessages, AdaptiveRequestMode

def basic_example():
    """Basic usage example"""
    print("=== Basic LLM Library Example ===")
    
    # Create messages
    messages = LLMMessages()
    messages = messages.build("You are a helpful assistant.", messages.SYSTEM)
    messages = messages.build("What is the capital of France?", messages.USER)
    
    print(f"Created {len(messages.messages)} messages")
    print(f"Estimated tokens: {messages.token_count}")
    
    # Display messages
    for i, msg in enumerate(messages.messages):
        print(f"Message {i+1}: {msg['role']} - {msg['content']}")

def request_modes_example():
    """Demonstrate different request modes"""
    print("\n=== Request Modes Example ===")
    
    modes = {
        "Precision": AdaptiveRequestMode.precision_mode(),
        "Balanced": AdaptiveRequestMode.balanced_mode(),
        "Creative": AdaptiveRequestMode.controlled_creative_mode(),
        "Exploratory": AdaptiveRequestMode.exploratory_mode(),
    }
    
    for name, mode in modes.items():
        print(f"{name} Mode - temp: {mode.temperature}, top_p: {mode.top_p}")

def llm_facade_example():
    """Example with LLM facade (requires API key)"""
    print("\n=== LLM Facade Example ===")
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set - skipping API example")
        return
    
    try:
        # Initialize LLM facade
        llm = LLM()
        
        # Create messages
        messages = LLMMessages()
        messages = messages.build("You are a helpful assistant.", messages.SYSTEM)
        messages = messages.build("Say hello in exactly 3 words.", messages.USER)
        
        # Use precision mode for deterministic response
        mode = AdaptiveRequestMode.precision_mode()
        
        print("Calling LLM with precision mode...")
        # Note: This would make an actual API call
        # response = llm.do_string_completion(messages.messages, mode=mode)
        # print(f"Response: {response}")
        print("(API call would happen here)")
        
    except Exception as e:
        print(f"Error: {e}")

def structured_output_example():
    """Example of structured outputs with instructor"""
    print("\n=== Structured Output Example ===")
    
    try:
        from pydantic import BaseModel
        
        class Person(BaseModel):
            name: str
            age: int
            city: str
        
        messages = LLMMessages()
        messages = messages.build("Extract person info as structured data.", messages.SYSTEM)
        messages = messages.build("John is 25 years old and lives in Paris.", messages.USER)
        
        print("Messages created for structured extraction")
        print("Would use: llm.do_instructor(messages.messages, Person)")
        print("Result would be a Person object with name='John', age=25, city='Paris'")
        
    except ImportError:
        print("Pydantic not available for this example")

if __name__ == "__main__":
    basic_example()
    request_modes_example()
    llm_facade_example()
    structured_output_example()
    
    print("\n=== Example Complete ===")
    print("For actual API usage, set OPENAI_API_KEY environment variable")