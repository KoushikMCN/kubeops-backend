from typing import TypedDict

class PodEvent(TypedDict):
    type: str | None
    reason: str | None
    message: str | None
    count: int | None
    last_timestamp: str | None