from typing import TypedDict

class PodInfo(TypedDict):
    name: str
    namespace: str
    labels: dict[str, str]
    status: str | None
    node_name: str | None