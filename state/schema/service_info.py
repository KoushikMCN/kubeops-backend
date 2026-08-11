from typing import TypedDict

class ServicePortInfo(TypedDict):
    port: int
    target_port: int | str
    protocol: str
    node_port: int | None


class ServiceInfo(TypedDict):
    name: str
    namespace: str
    labels: dict[str, str] | None
    annotations: dict[str, str] | None

    type: str
    cluster_ip: str | None

    selector: dict[str, str]

    ports: list[ServicePortInfo]

    external_ips: list[str] | None
    load_balancer_ip: str | None

    creation_timestamp: str | None