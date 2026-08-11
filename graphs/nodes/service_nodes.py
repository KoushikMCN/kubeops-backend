import os

from services.kubernetes.svc_service import SvcService
from services.kubernetes.pod_service import PodService

from state.service_connectivity_state import ServiceConnectivityState
from mappers.svc_mapper import service_to_dict
from mappers.pod_mapper import pod_to_dict

from langchain_google_genai import ChatGoogleGenerativeAI

service_service = SvcService()
pod_service = PodService()

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)


def get_service_node(
    state: ServiceConnectivityState,
) -> ServiceConnectivityState:
    """
    Fetch the service.
    """

    service = service_service.describe_service(
        name=state["service_name"],
        namespace=state["namespace"],
    )

    state["service"] = service_to_dict(service)

    return state


def get_endpoints_node(
    state: ServiceConnectivityState,
) -> ServiceConnectivityState:
    """
    Fetch service endpoints.
    """

    endpoints = service_service.get_service_endpoints(
        name=state["service_name"],
        namespace=state["namespace"],
    )

    state["endpoints"] = endpoints

    return state


def list_matching_pods_node(
    state: ServiceConnectivityState,
) -> ServiceConnectivityState:
    """
    List pods selected by the service selector.
    """

    selector = state["service"]["selector"] if state["service"] else {}

    label_selector = ",".join(
        f"{k}={v}"
        for k, v in selector.items()
    )

    pod_list = pod_service.list_pods(
        namespace=state["namespace"],
        label_selector=label_selector,
    )

    state["pods"] = [
        pod_to_dict(pod)
        for pod in (pod_list.items or [])
    ]

    return state


def diagnose_service_node(
    state: ServiceConnectivityState,
) -> ServiceConnectivityState:
    """
    Diagnose service connectivity issues.
    """

    prompt = f"""
You are a Kubernetes expert.

Diagnose why this Service may not be routing traffic.

Service:
{state["service"]}

Endpoints:
{state["endpoints"]}

Pods:
{state["pods"]}

Return:

1. Root Cause
2. Evidence
3. Suggested Fix
"""

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, str):
        state["diagnosis"] = content
    else:
        state["diagnosis"] = "\n".join(
            part if isinstance(part, str) else str(part)
            for part in content
        )

    return state