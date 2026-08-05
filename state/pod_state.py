from typing import TypedDict


class PodInfo(TypedDict):
    name: str
    namespace: str
    labels: dict[str, str]
    status: str | None
    node_name: str | None

class PodEvent(TypedDict):
    type: str | None
    reason: str | None
    message: str | None
    count: int | None
    last_timestamp: str | None