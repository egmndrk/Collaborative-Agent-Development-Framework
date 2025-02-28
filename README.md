# Multi-Agent Software Development Framework

A collaborative software development framework that uses multiple LLM agents to automate the software development lifecycle from requirements gathering to code generation and testing.

## Overview

This project implements a multi-agent system using Google's Gemini API to automate software development phases:

1. **Requirements Analysis** - A dedicated agent interviews the user to gather software requirements
2. **Code Generation** - A developer agent writes Python code based on the gathered requirements
3. **Testing** - A tester agent evaluates the code and provides feedback
4. **Iterative Improvement** - The system iterates through testing and code revision until requirements are satisfied

## Features

- Automated requirements gathering through interactive questioning
- Automatic generation of Python code based on requirements
- Automated testing and code improvement
- Token usage tracking for each agent
- Configurable iteration limits to control the development process

## Dependencies

- Python 3.x
- Google Generative AI Python SDK
- python-dotenv

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/egmndrk/Collaborative-Agent-Development-Framework.git
   cd Collaborative-Agent-Development-Framework
   ```

2. Install the required packages:
   ```
   pip install google-generativeai python-dotenv
   ```

3. Create a `.env` file in the project root directory with your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

Run the main script to start the software development process:

```
python CollaborativeAgentDevFramework.py
```

The system will:
1. Start a conversation with the Requirements Analyst to gather your software requirements
2. Generate an SRS (Software Requirements Specification) document
3. Create Python code that meets those requirements
4. Test the code against the requirements
5. Refine the code based on test feedback (up to 3 iterations)
6. Track and report token usage for each agent

## Agent Roles

### Requirements Analyst
Conducts an interview with the user to gather software requirements, asking specific questions about:
- Main purpose/objective
- Key features needed
- Performance requirements
- Constraints or limitations

### Coder
Generates clean, well-documented Python code that follows PEP 8 guidelines and includes appropriate error handling based on the requirements specification.

### Tester
Reviews the generated code against the original requirements, identifying issues or confirming that all requirements have been met.

## Customization

You can modify the system by:
- Adjusting the agent prompt templates in the role string variables
- Changing the maximum number of interactions in the requirements gathering phase
- Modifying the number of testing and revision iterations
- Using different Gemini models for specific agents
