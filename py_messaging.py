# 05_messages.py
import os
import asyncio
from dotenv import load_dotenv               # reads the .env file
from autogen_agentchat.agents import AssistantAgent
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
                           system_message="You are helpful and concise.")

    result = await agent.run(task="What is 15 times 12, and explain briefly?")

    # result.messages is a LIST of every message in the run
    print("Total messages:", len(result.messages))
    print("-" * 40)

    # loop through and inspect each one
    for i, message in enumerate(result.messages):
        # .source = who sent it, type(message).__name__ = the message class, .content = the text
        print(f"[{i}] from '{message.source}' | type: {type(message).__name__}")
        print(f"    content: {message.content}")

    print("-" * 40)
    # the final answer is always the LAST message
    print("FINAL ANSWER:", result.messages[-1].content)
    # why the run stopped
    print("STOP REASON:", result.stop_reason)

    await model_client.close()

asyncio.run(main())