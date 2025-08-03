# Guardrails

A Python project demonstrating AI agent guardrails using the `openai-agents` library with Google's Gemini model. This project showcases both input and output guardrails to control AI agent behavior.

## Features

- **Input Guardrails**: Prevent agents from processing certain types of input (e.g., political questions)
- **Output Guardrails**: Monitor and control agent outputs (e.g., prevent mathematical calculations)
- **Gemini Integration**: Uses Google's Gemini 2.5 Flash model via OpenAI-compatible API
- **Async Support**: Full asynchronous operation for better performance
- **Structured Outputs**: Uses Pydantic models for type-safe outputs

## Project Structure

```
Guradrails/
├── main.py              # Input guardrail example (politics detection)
├── output_grdrail.py    # Output guardrail example (math detection)
├── pyproject.toml       # Project configuration and dependencies
├── README.md           # This file
└── uv.lock             # Dependency lock file
```

## Examples

### Input Guardrail (`main.py`)
Demonstrates how to prevent an agent from processing political questions:

```python
@input_guardrail
async def politics_guardrail(ctx, agent, input):
    # Checks if input contains political content
    # Triggers guardrail if politics detected
```

### Output Guardrail (`output_grdrail.py`)
Shows how to monitor agent outputs and prevent mathematical calculations:

```python
@output_guardrail
async def math_guardrail(ctx, agent, output):
    # Checks if output contains mathematical content
    # Triggers guardrail if math detected
```

## Prerequisites

- Python 3.12 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Guradrails
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

### Running Input Guardrail Example
```bash
python main.py
```

This will demonstrate the politics guardrail by attempting to ask a political question, which should trigger the guardrail.

### Running Output Guardrail Example
```bash
python output_grdrail.py
```

This will demonstrate the math guardrail by asking the agent to solve a mathematical equation, which should trigger the output guardrail.

## Dependencies

- `openai-agents>=0.2.4`: Core AI agent framework
- `python-dotenv>=1.1.1`: Environment variable management
- `pydantic`: Data validation and settings management
- `openai`: OpenAI-compatible client for Gemini API

## Configuration

The project uses the following configuration:

- **Model**: Gemini 2.5 Flash
- **API Base URL**: `https://generativelanguage.googleapis.com/v1beta/openai/`
- **Tracing**: Enabled for debugging
- **Logging**: Verbose stdout logging enabled

## How Guardrails Work

### Input Guardrails
Input guardrails are triggered before the main agent processes the input. They can:
- Analyze the input content
- Decide whether to allow processing
- Throw `InputGuardrailTripwireTriggered` exception if triggered

### Output Guardrails
Output guardrails are triggered after the main agent generates a response. They can:
- Analyze the output content
- Decide whether to allow the output
- Throw `OutputGuardrailTripwireTriggered` exception if triggered

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions, please open an issue on the repository.
