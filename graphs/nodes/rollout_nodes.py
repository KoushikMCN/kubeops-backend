from services.kubernetes.deployment_service import DeploymentService
from state.rollout_state import RolloutState
from mappers.deployment_mapper import deployment_to_dict


deployment_service = DeploymentService()


def get_deployment_node(
    state: RolloutState,
) -> RolloutState:
    """
    Fetch the deployment that is being rolled out.
    """

    deployment = deployment_service.get_deployment(
        namespace=state["namespace"],
        deployment_name=state["deployment_name"],
    )

    state["deployment"] = deployment_to_dict(deployment)

    return state


def get_rollout_status_node(
    state: RolloutState,
) -> RolloutState:
    """
    Check the current rollout status of the deployment.
    """

    deployment = deployment_service.rollout_status(
        namespace=state["namespace"],
        deployment_name=state["deployment_name"],
    )

    status = deployment.status

    conditions = {
        c.type: c
        for c in (status.conditions if status else [])
    }

    progressing = conditions.get("Progressing")
    available = conditions.get("Available")

    if (
        progressing
        and progressing.status == "True"
        and available
        and available.status == "True"
    ):
        rollout_status = "complete"

    elif (
        progressing
        and progressing.status == "False"
    ):
        rollout_status = "failed"

    else:
        rollout_status = "progressing"

    if deployment.status is None:
        state["rollout_status"] = "unknown"

    state["rollout_status"] = rollout_status
    
    return state


def rollout_result_node(
    state: RolloutState,
) -> RolloutState:
    """
    Determine the final rollout result.
    """

    rollout_status = state["rollout_status"]

    if rollout_status == "complete":
        state["rollout_message"] = (
            f"Deployment '{state['deployment_name']}' "
            "rollout completed successfully."
        )

    elif rollout_status == "progressing":
        state["rollout_message"] = (
            f"Deployment '{state['deployment_name']}' "
            "rollout is still in progress."
        )

    else:
        state["rollout_message"] = (
            f"Deployment '{state['deployment_name']}' "
            f"rollout status: {rollout_status}."
        )

    return state