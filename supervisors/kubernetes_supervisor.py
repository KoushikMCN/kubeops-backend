import os

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from agents.kubernetes_agent import build_kubernetes_agent
from graphs.deployment_diagnosis import build_deployment_diagnosis_graph

deployment_graph = build_deployment_diagnosis_graph()
kubernetes_agent = build_kubernetes_agent()


@tool
def kubernetes_crud(query: str) -> str:
    """
    Perform Kubernetes CRUD and inspection operations.

    Use this for:
    - create
    - delete
    - update
    - patch
    - list
    - get
    - describe
    - logs
    - events
    - scaling
    - restart
    """

    response = kubernetes_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }
    )

    return response["messages"][-1].content


@tool
def deployment_diagnosis(
    deployment_name: str,
    namespace: str = "default",
) -> str:
    """
    Diagnose why a Kubernetes deployment is unhealthy.
    """

    result = deployment_graph.invoke(
        {
            "deployment_name": deployment_name,
            "namespace": namespace,
            "deployment": None,
            "pods": [],
            "pod_events": {},
            "pod_logs": {},
            "diagnosis": "",
        }
    )

    if result.get("error"):
        return result["error"]

    return result["diagnosis"]

model = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

supervisor = create_agent(
    model=model,
    tools=[
        kubernetes_crud,
        deployment_diagnosis,
    ],
    system_prompt="""
You are the supervisor for a Kubernetes AI assistant.

You have two tools:

1. kubernetes_crud
- Use for creating, deleting, updating, listing, describing, scaling, restarting and inspecting Kubernetes resources.

2. deployment_diagnosis
- Use ONLY when the user wants to diagnose or troubleshoot a deployment.

Choose exactly one tool.
Never diagnose when the user wants CRUD.
Never use CRUD when the user explicitly asks for deployment diagnosis.

## When a tool returns the final answer, return it verbatim without modification.
""",
)