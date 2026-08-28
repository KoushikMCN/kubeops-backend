import os

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from agents.kubernetes_agent import build_kubernetes_agent
from graphs.deployment_diagnosis import build_deployment_diagnosis_graph
from graphs.deployment_rollout import build_deployment_rollout_status_graph
from graphs.cluster_health import build_cluster_health_graph
from graphs.service_connectivity import build_service_connectivity_graph

deployment_graph = build_deployment_diagnosis_graph()
kubernetes_agent = build_kubernetes_agent()
deployment_rollout_graph = build_deployment_rollout_status_graph()
cluster_health_graph = build_cluster_health_graph()
service_connectivity_graph = build_service_connectivity_graph()


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

@tool
def deployment_rollout(
    deployment_name: str,
    namespace: str = "default",
) -> str:
    """
    Check the rollout status of a Kubernetes deployment.
    Use this to determine whether a deployment rollout is successful,
    in progress, or failing.
    """

    result = deployment_rollout_graph.invoke(
        {
            "deployment_name": deployment_name,
            "namespace": namespace,
            "deployment": None,
            "rollout_status": None,
            "rollout_message": None,
        }
    )

    return result["rollout_message"]


@tool
def cluster_health(
    namespace: str = "default",
) -> str:
    """
    Check the overall health of a Kubernetes namespace.
    Use this to identify unhealthy deployments, pods, services,
    and relevant Kubernetes events.
    """

    result = cluster_health_graph.invoke(
        {
            "namespace": namespace,
            "deployments": [],
            "pods": [],
            "services": [],
            "events": [],
            "diagnosis": None,
        }
    )

    return result["diagnosis"]


@tool
def service_connectivity(
    service_name: str,
    namespace: str = "default",
) -> str:
    """
    Diagnose why a Kubernetes Service may not be reachable
    or routing traffic correctly.
    """

    result = service_connectivity_graph.invoke(
        {
            "service_name": service_name,
            "namespace": namespace,
            "service":  None,
            "endpoints": [],
            "pods": [],
            "diagnosis": None,
            "error": None
        }
    )

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
        deployment_rollout,
        cluster_health,
        service_connectivity,
    ],
    system_prompt="""
You are the supervisor for a Kubernetes AI assistant.

Choose the appropriate tool or tools to answer the user's request.

You may call multiple tools sequentially when necessary.

After each tool result, decide whether:
1. The user's request has been fully answered -> return the answer.
2. More investigation is needed -> call another relevant tool.

Do not call tools unnecessarily.

Tool usage:

- kubernetes_crud:
  Create, delete, update, list, describe, scale, restart, and inspect
  Kubernetes resources.

- deployment_diagnosis:
  Diagnose why a specific deployment is unhealthy.

- deployment_rollout:
  Check whether a deployment rollout is successful, in progress, or failing.

- service_connectivity:
  Diagnose why a Kubernetes Service is unreachable or has connectivity issues.

- cluster_health:
  Assess the overall health of a cluster or namespace.

Use evidence from previous tool results when deciding whether another
tool should be called.

When sufficient information has been collected, provide the final answer.
""",
)