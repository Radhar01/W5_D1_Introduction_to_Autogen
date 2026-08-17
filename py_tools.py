# 07_tools.py
import os
import asyncio
from dotenv import load_dotenv               # reads the .env file
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily

load_dotenv()   # load GROQ_API_KEY from the .env file

# ---- the tool: a plain function with type hints + a clear docstring ----
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # (a real version would call a weather API; we fake it for the demo)
    return f"The weather in {city} is 31 degrees Celsius and sunny."

async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],       # value comes from .env
        base_url="https://api.openai.com/v1",
        model_info={"vision": False, "function_calling": True, "json_output": True,
                    "family": ModelFamily.UNKNOWN, "structured_output": True},
        include_name_in_message=False,
    )

    agent = AssistantAgent(
        name="weather_agent",
        model_client=model_client,
        tools=[get_weather],              # hand the tool to the agent
        reflect_on_tool_use=True,         # turn the raw tool result into a clean sentence
        system_message="You help users check the weather. Use your tools when asked.",
    )

    # stream it so you can SEE the tool being called
    await Console(agent.run_stream(task="What's the weather in Chennai right now?"))

    await model_client.close()

asyncio.run(main())