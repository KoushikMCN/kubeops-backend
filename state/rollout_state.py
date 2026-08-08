from typing import TypedDict

from state.deployment_state import DeploymentInfo


class RolloutState(TypedDict):
    deployment_name: str
    namespace: str

    deployment: DeploymentInfo | None

    rollout_status: str | None
    rollout_message: str | None