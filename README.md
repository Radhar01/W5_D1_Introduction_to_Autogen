# W5_D1 — Introduction to AutoGen

Beginner-friendly walkthrough of Microsoft's [AutoGen](https://microsoft.github.io/autogen/) framework, built with `autogen-agentchat` and `autogen-ext`. Each script is a small, self-contained example that introduces one new concept, using an OpenAI (`gpt-4o-mini`) chat completion client as the agent's "brain".

## Prerequisites

- Python 3.10+
- An OpenAI API key (some scripts reference a Groq key as an alternative model provider)

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

2. Install dependencies:

   ```bash
   pip install autogen-agentchat autogen-ext[openai] python-dotenv
   ```

3. Create a `.env` file in the project root with your API key(s) (this file is git-ignored and must never be committed):

   ```
   OPENAI_API_KEY="your-openai-key-here"
   GROQ_API_KEY="your-groq-key-here"
   ```

## Scripts

| File | Concept | Description |
|---|---|---|
| [py_intro_autogen.py](py_intro_autogen.py) | Hello World | The smallest working AutoGen program — builds a model client and a single `AssistantAgent`, then asks it one question. |
| [py_configuring_llm.py](py_configuring_llm.py) | Model client | Talks to the LLM directly via `model_client.create()` (no agent), showing raw `UserMessage` input and inspecting the response content and token usage. |
| [py_first_agent.py](py_first_agent.py) | System message | Creates an `AssistantAgent` with a `system_message` to give it a persona ("friendly coding tutor") and standing instructions. |
| [py_prompt_engineering.py](py_prompt_engineering.py) | Prompt engineering | Runs the same question through a vaguely-prompted agent and a precisely-prompted agent (role, rules, format) to compare output quality. |
| [py_messaging.py](py_messaging.py) | Messages & run results | Inspects `result.messages` — the full list of messages in a run — printing each message's source, type, and content, plus the final answer and stop reason. |
| [py_observing_agents.py](py_observing_agents.py) | Streaming output | Uses `agent.run_stream()` with `Console()` to watch an agent's response stream in real time instead of waiting for the full result. |
| [py_tools.py](py_tools.py) | Tool use | Gives an agent a Python function (`get_weather`) as a tool, with `reflect_on_tool_use=True` so it turns raw tool output into a natural-language reply. |
| [py_Custom_tools.py](py_Custom_tools.py) | Custom tools | A finance agent equipped with two custom tools — `add_numbers` and an EMI loan calculator — that it must use instead of guessing numbers. |

## Running

Each file is a standalone script:

```bash
python py_intro_autogen.py
```

## Notes

- All scripts load credentials from `.env` via `python-dotenv`; the `.env` file itself is excluded from version control (see `.gitignore`).
- `model_info` is set manually since these examples use `ModelFamily.UNKNOWN`, telling AutoGen the model supports function calling, JSON output, and structured output.
