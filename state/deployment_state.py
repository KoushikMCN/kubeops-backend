from typing import Any, TypedDict
from .pod_state import PodEvent
from .schema.deployment_info import DeploymentInfo
from .schema.pod_info import PodInfo

class DeploymentDiagnosisState(TypedDict):
    deployment_name: str
    namespace: str

    deployment: DeploymentInfo | None

    pods: list[PodInfo]

    pod_events: dict[str, list[PodEvent]]

    pod_logs: dict[str, str]

    diagnosis: str | list[str | dict[Any, Any]]