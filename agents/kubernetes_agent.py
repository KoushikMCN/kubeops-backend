import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.pod_tools import create_pod, get_pod_logs, list_pods, get_pod, delete_pod, get_pod_events

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
        tools=[list_pods, get_pod_logs, create_pod, get_pod, delete_pod, get_pod_events],
        system_prompt=SYSTEM_PROMPT.strip(),
    )
