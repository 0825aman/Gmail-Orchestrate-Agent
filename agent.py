"""
agent.py
--------
Builds and runs the LangGraph ReAct agent powered by IBM WatsonX
(ibm/granite-3-3-8b-instruct) and the four Gmail tools.

Uses:
  - langchain_ibm.ChatWatsonx  (chat model with native tool-calling)
  - langgraph.prebuilt.create_react_agent  (LangGraph v1.2+)

Usage:
    from agent import run_agent
    reply = run_agent("List my last 5 emails")
"""

import os
from dotenv import load_dotenv

from langchain_ibm import ChatWatsonx
from langgraph.prebuilt import create_react_agent

from gmail_tools import get_tools

# Load .env → WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL
load_dotenv()

# ---------------------------------------------------------------------------
# WatsonX Chat Model
# ---------------------------------------------------------------------------

llm = ChatWatsonx(
    model_id="ibm/granite-4-h-small",
    url=os.environ["WATSONX_URL"],
    apikey=os.environ["WATSONX_API_KEY"],
    project_id=os.environ["WATSONX_PROJECT_ID"],
    params={
        "max_new_tokens": 1024,
        "temperature": 0,
    },
)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a helpful Gmail assistant. "
    "Use the available tools to carry out the user's request about their Gmail inbox. "
    "When listing emails, always display the sender, subject, date, and message ID for each email. "
    "Be concise and clear in your final answer."
)

# ---------------------------------------------------------------------------
# Agent (LangGraph ReAct — tool-calling)
# ---------------------------------------------------------------------------

tools = get_tools()

agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT,
)


def run_agent(user_message: str) -> str:
    """
    Run the Gmail agent with a natural language message.

    Args:
        user_message: Natural language instruction, e.g. "list my last 5 emails".

    Returns:
        The agent's final plain-text answer.
    """
    result = agent_executor.invoke(
        {"messages": [{"role": "user", "content": user_message}]}
    )
    # The final answer is the last AI message in the messages list
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            return msg.content
    return "The agent did not return an answer."
