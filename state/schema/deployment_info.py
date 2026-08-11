from typing import TypedDict

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