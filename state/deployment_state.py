from typing import Any, TypedDict
from .pod_state import PodInfo, PodEvent

class DeploymentInfo(TypedDict):
    name: str
    namespace: str
    labels: dict[str, str] | None
    selector: dict[str, str]
    annotations: dict[str, str] | None
    replicas: int | None
    ready_replicas: int | None
    available_replicas: int | None
    updated_replicas: int | None
    conditions: list[dict]

class DeploymentDiagnosisState(TypedDict):
    deployment_name: str
    namespace: str

    deployment: DeploymentInfo | None

    pods: list[PodInfo]

    pod_events: dict[str, list[PodEvent]]

    pod_logs: dict[str, str]

    diagnosis: str | list[str | dict[Any, Any]]