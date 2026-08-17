# 02_configuring_llm.py
import os
import asyncio
from dotenv import load_dotenv               # reads the .env file
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily, UserMessage

load_dotenv()   # load OPENAI_API_KEY from the .env file into the environment

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

    # talk to the model DIRECTLY (no agent) using .create()
    # every low-level message needs a "source" saying who sent it
    response = await model_client.create(
        [UserMessage(content="What is the capital of Tamil Nadu?", source="user")]
    )

    # the model's text is in response.content
    print("Model replied:", response.content)
    # you can also inspect token usage
    print("Tokens used:", response.usage)

    await model_client.close()

asyncio.run(main())