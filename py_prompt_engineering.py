# 04_prompt_engineering.py
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

    the_question = "Tell me about electric cars."

    # AGENT A: a vague system_message
    agent_a = AssistantAgent(
        name="vague_agent",
        model_client=model_client,
        system_message="You are an assistant.",
    )

    # AGENT B: a specific, well-engineered system_message (Role, Rules, Format)
    agent_b = AssistantAgent(
        name="specific_agent",
        model_client=model_client,
        system_message=(
            "ROLE: You are an auto-industry analyst.\n"
            "RULES: Be factual, no hype.\n"
            "FORMAT: Reply as exactly 3 short bullet points, each under 15 words."
        ),
    )

    # run the SAME question through both
    result_a = await agent_a.run(task=the_question)
    result_b = await agent_b.run(task=the_question)

    print("===== VAGUE PROMPT =====")
    print(result_a.messages[-1].content)
    print("\n===== ENGINEERED PROMPT =====")
    print(result_b.messages[-1].content)

    await model_client.close()

asyncio.run(main())