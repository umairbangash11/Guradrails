from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)
import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, handoff
from agents.run import RunConfig
from agents import enable_verbose_stdout_logging
from openai import AsyncOpenAI

load_dotenv()

enable_verbose_stdout_logging()

# Load .env Variables
load_dotenv()

# Get Gemini API Key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Initialize Gemini Client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Gemini Model Setup
model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash",
)

# RunConfig

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=False,
      # Add this line
)

class MessageOutput(BaseModel): 
    response: str

class MathOutput(BaseModel): 
    reasoning: str
    is_math: bool

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
    model=model,
)

@output_guardrail
async def math_guardrail(  
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
    )

agent = Agent( 
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail],
    output_type=MessageOutput,
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?", run_config=config)
        print("Guardrail didn't trip - this is unexpected")

    except OutputGuardrailTripwireTriggered:
        print("Math output guardrail tripped")

if __name__ == "__main__":
    asyncio.run(main())