from typing import TypedDict

from state.schema.deployment_info import DeploymentInfo
from state.schema.pod_info import PodInfo
from state.schema.service_info import ServiceInfo


class ClusterHealthState(TypedDict):
    namespace: str | None

    deployments: list[DeploymentInfo]
    pods: list[PodInfo]
    services: list[ServiceInfo]

    events: list[dict]

    diagnosis: str | None