# 03_first_agent.py
import os
import asyncio
from dotenv import load_dotenv               # reads the .env file
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily

load_dotenv()   # load GROQ_API_KEY from the .env file

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

    # system_message = the agent's standing instructions (its personality/rules)
    agent = AssistantAgent(
        name="tutor",
        model_client=model_client,
        system_message="You are a friendly coding tutor. Explain simply and use one short example.",
    )

    # task = the specific request for this run
    result = await agent.run(task="Explain what a Python list is.")
    print(result.messages[-1].content)

    await model_client.close()

asyncio.run(main())