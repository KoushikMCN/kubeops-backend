import os

from mappers.deployment_mapper import deployment_to_dict
from mappers.pod_mapper import pod_to_dict
from services.kubernetes.deployment_service import DeploymentService
from services.kubernetes.pod_service import PodService
from state.deployment_state import DeploymentDiagnosisState
from state.pod_state import PodEvent

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from kubernetes.client.rest import ApiException

deployment_service = DeploymentService()
pod_service = PodService()

HEALTHY_POD_STATUSES = {
    "Running",
    "Succeeded",
}

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

def get_deployment_node(
    state: DeploymentDiagnosisState,
) -> DeploymentDiagnosisState:
    """
    Fetch the deployment and store it in the graph state.
    """

    deployment = deployment_service.get_deployment(
        namespace=state["namespace"],
        deployment_name=state["deployment_name"],
    )

    state["deployment"] = deployment_to_dict(deployment)

    return state

def list_pods_node(
    state: DeploymentDiagnosisState,
) -> DeploymentDiagnosisState:
    """
    Fetch all pods belonging to the deployment and store them in the graph state.
    """

    deployment = state["deployment"]
    assert deployment is not None

    selector = deployment["selector"]

    pod_list = pod_service.list_pods(state["namespace"])

    pods = []

    for pod in (pod_list.items or []):
        pod_info = pod_to_dict(pod)

        if not all(
            pod_info["labels"].get(k) == v
            for k, v in selector.items()
        ):
            continue

        pods.append(pod_info)

    state["pods"] = pods
    return state

def get_events_node(
    state: DeploymentDiagnosisState,
) -> DeploymentDiagnosisState:
    """
    Fetch Kubernetes events for all pods belonging to the deployment.
    """

    pod_events: dict[str, list[PodEvent]] = {}

    for pod in state["pods"]:
        events = pod_service.get_pod_events(
            namespace=pod["namespace"],
            pod_name=pod["name"],
        )

        pod_events[pod["name"]] = events

    state["pod_events"] = pod_events

    return state

def get_logs_node(
    state: DeploymentDiagnosisState,
) -> DeploymentDiagnosisState:
    """
    Fetch logs for unhealthy pods belonging to the deployment.
    """

    pod_logs: dict[str, str] = {}

    for pod in state["pods"]:
        status = pod["status"]

        if status in HEALTHY_POD_STATUSES:
            continue

        try:
            logs = pod_service.get_pod_logs(
                name=pod["name"],
                namespace=pod["namespace"],
            )

        except ApiException as e:
            if e.status == 400:
                logs = (
                    "Container has not started yet. "
                    "Logs are unavailable."
                )
            else:
                logs = str(e)

        pod_logs[pod["name"]] = logs

    state["pod_logs"] = pod_logs

    return state

def diagnosis_node(
    state: DeploymentDiagnosisState,
) -> DeploymentDiagnosisState:
    """
    Analyze the deployment state and determine the root cause.
    """

    prompt = f"""
You are an experienced Kubernetes Site Reliability Engineer.

Analyze the following deployment.

Deployment:
{state["deployment"]}

Pods:
{state["pods"]}

Pod Events:
{state["pod_events"]}

Pod Logs:
{state["pod_logs"]}

Your response must contain:

1. Root Cause
2. Evidence
3. Suggested Fix

Be concise and technical.
"""

    response = llm.invoke(
        [
            HumanMessage(content=prompt),
        ]
    )

    state["diagnosis"] = response.content

    return state