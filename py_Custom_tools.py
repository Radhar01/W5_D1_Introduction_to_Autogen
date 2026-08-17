# 08_custom_tools.py
import os
import asyncio
from dotenv import load_dotenv               # reads the .env file
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily

load_dotenv()   # load GROQ_API_KEY from the .env file

# ---- custom tool 1: simple addition ----
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together and return the sum."""
    return a + b

# ---- custom tool 2: loan EMI calculator ----
def calculate_emi(principal: float, annual_rate: float, months: int) -> float:
    """Calculate the monthly EMI for a loan.
    principal = loan amount, annual_rate = yearly interest percent, months = tenure in months.
    """
    monthly_rate = (annual_rate / 100) / 12          # convert yearly % to monthly decimal
    emi = principal * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
    return round(emi, 2)                             # round to 2 decimals for money
"""
async def main():
    model_client = OpenAIChatCompletionClient(
        model="llama-3.3-70b-versatile",
        api_key=os.environ["GROQ_API_KEY"],       # value comes from .env
        base_url="https://api.groq.com/openai/v1",
        model_info={"vision": False, "function_calling": True, "json_output": True,
                    "family": ModelFamily.UNKNOWN, "structured_output": True},
        include_name_in_message=False,
    )
"""

async def main():
    # build the "brain" (OpenAI)
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],       # value comes from .env
        base_url="https://api.openai.com/v1",
        model_info={"vision": False, "function_calling": True, "json_output": True,
                    "family": ModelFamily.UNKNOWN, "structured_output": True},
        include_name_in_message=False,
    )

    agent = AssistantAgent(
        name="finance_agent",
        model_client=model_client,
        tools=[add_numbers, calculate_emi],     # give it BOTH tools
        reflect_on_tool_use=True,
        system_message="You are a finance helper. Always use your tools for calculations; never guess numbers.",
    )

    await Console(agent.run_stream(
        task="What's the monthly EMI on a 500000 loan at 9% annual interest over 24 months?"
    ))

    await model_client.close()

asyncio.run(main())