import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.registry import tools

SYSTEM_PROMPT = """
You are a Kubernetes assistant for this project.
Use only the available tools when they help answer the user's request.
If the available tools are insufficient, say what is missing plainly.
"""


def build_kubernetes_agent():
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT.strip(),
    )
