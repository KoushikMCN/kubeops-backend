from typing import TypedDict
from .schema.pod_info import PodInfo
from .schema.service_info import ServiceInfo

class ServiceConnectivityState(TypedDict):
    service_name: str
    namespace: str

    service: ServiceInfo | None

    endpoints: list[str]

    pods: list[PodInfo]

    diagnosis: str | None

    error: str | None