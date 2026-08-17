# 01_intro.py  — the smallest working AutoGen program
import os
import asyncio
from dotenv import load_dotenv               # reads the .env file
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily

load_dotenv()   # load OPENAI_API_KEY from the .env file into the environment

async def main():
    # build the "brain" (openAI here)
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],       # value comes from .env
        base_url="https://api.openai.com/v1",
        model_info={"vision": False, "function_calling": True, "json_output": True,
                    "family": ModelFamily.UNKNOWN, "structured_output": True},
        include_name_in_message=False,
    )

    # the simplest agent: just a name + the brain
    agent = AssistantAgent(name="assistant", model_client=model_client)

    # ask one thing and print the reply
    result = await agent.run(task="Say hello and tell me what an AI agent is in one sentence.")
    print(result.messages[-1].content)

    await model_client.close()

asyncio.run(main())