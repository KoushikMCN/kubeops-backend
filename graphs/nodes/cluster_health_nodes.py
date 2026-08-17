import os
from dotenv import load_dotenv
from typing import cast

from services.kubernetes.deployment_service import DeploymentService
from services.kubernetes.pod_service import PodService
from services.kubernetes.svc_service import SvcService
from services.kubernetes.client import core_v1

from state.cluster_health_state import ClusterHealthState

from mappers.deployment_mapper import deployment_to_dict
from mappers.pod_mapper import pod_to_dict
from mappers.svc_mapper import service_to_dict

from kubernetes.client import CoreV1EventList
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)


deployment_service = DeploymentService()
pod_service = PodService()
service_service = SvcService()


def get_deployments_node(
    state: ClusterHealthState,
) -> ClusterHealthState:
    """
    Get deployments for the requested namespace.
    """

    deployments = deployment_service.list_deployments(
        namespace=state["namespace"],
    )

    state["deployments"] = [
        deployment_to_dict(deployment)
        for deployment in (deployments.items or [])
    ]

    return state


def get_pods_node(
    state: ClusterHealthState,
) -> ClusterHealthState:
    """
    Get pods for the requested namespace.
    """

    pods = pod_service.list_pods(
        namespace=state["namespace"],
    )

    state["pods"] = [
        pod_to_dict(pod)
        for pod in (pods.items or [])
    ]

    return state


def get_services_node(
    state: ClusterHealthState,
) -> ClusterHealthState:
    """
    Get services for the requested namespace.
    """

    services = service_service.list_services(
        namespace=state["namespace"],
    )

    state["services"] = [
        service_to_dict(service)
        for service in (services.items or [])
    ]

    return state


def get_events_node(
    state: ClusterHealthState,
) -> ClusterHealthState:
    """
    Get Kubernetes events for the requested namespace.
    """

    if state["namespace"]:
        events = cast(
            CoreV1EventList,
            core_v1.list_namespaced_event(
                namespace=state["namespace"],
            ),
        )
    else:
        events = cast(
            CoreV1EventList,
            core_v1.list_event_for_all_namespaces(),
        )

    state["events"] = [
        {
            "name": event.metadata.name if event.metadata else None,
            "namespace": event.metadata.namespace if event.metadata else None,
            "type": event.type,
            "reason": event.reason,
            "message": event.message,
            "count": event.count,
        }
        for event in (events.items or [])
    ]

    return state


def diagnose_cluster_node(
    state: ClusterHealthState,
) -> ClusterHealthState:
    """
    Analyze the collected cluster information and produce
    an overall health assessment.
    """

    prompt = f"""
You are a Kubernetes operations expert.

Analyze the following Kubernetes cluster information and determine
the overall health of the cluster.

Deployments:
{state["deployments"]}

Pods:
{state["pods"]}

Services:
{state["services"]}

Recent Events:
{state["events"]}

Provide your response in this format:

1. Overall Health
- Healthy / Degraded / Critical

2. Issues
- List each detected issue.
- If there are no issues, explicitly say so.

3. Evidence
- Reference the Kubernetes resources and events that support your findings.

4. Recommendations
- Suggest concrete actions to resolve the detected issues.

Do not invent problems that are not supported by the provided data.
"""

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, str):
        state["diagnosis"] = content
    else:
        state["diagnosis"] = "".join(
            part["text"]
            for part in content
            if isinstance(part, dict) and part.get("type") == "text"
        )

    return state