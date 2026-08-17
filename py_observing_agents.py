# 06_observing.py
import os
import asyncio
from dotenv import load_dotenv               # reads the .env file
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily

load_dotenv()   # load GROQ_API_KEY from the .env file

async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],       # value comes from .env
        base_url="https://api.openai.com/v1",
        model_info={"vision": False, "function_calling": True, "json_output": True,
                    "family": ModelFamily.UNKNOWN, "structured_output": True},
        include_name_in_message=False,
    )

    agent = AssistantAgent(name="assistant", model_client=model_client,
                           system_message="You are a helpful explainer.")

    # run_stream() emits messages as they happen; Console() prints them nicely in real time
    await Console(agent.run_stream(task="Explain how the internet works, step by step."))

    await model_client.close()

asyncio.run(main())