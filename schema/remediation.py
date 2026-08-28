from typing import Any, Literal

from pydantic import BaseModel


class RemediationTarget(BaseModel):
    resource_type: str
    resource_name: str
    namespace: str


class RemediationPlan(BaseModel):
    action: str
    target: RemediationTarget
    parameters: dict[str, Any]
    reason: str
    risk: Literal["low", "medium", "high"]