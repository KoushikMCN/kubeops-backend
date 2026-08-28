import os
from dotenv import load_dotenv
from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import interrupt

from schema.remediation import RemediationPlan
from state.remediation_state import RemediationState

load_dotenv()

model = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

remediation_planner = model.with_structured_output(RemediationPlan)


def create_remediation_plan_node(
    state: RemediationState,
) -> RemediationState:
    """
    Create a structured remediation plan from a Kubernetes diagnosis.
    """

    response = remediation_planner.invoke(
        [
            SystemMessage(
                content="""
You are a Kubernetes remediation planner.

Given a Kubernetes diagnosis, create exactly one remediation plan.

Choose an action that directly addresses the root cause.

Only choose from these supported actions:

- restart_deployment
- scale_deployment
- update_deployment_image
- update_deployment_command
- update_service_selector

Do not invent new actions.

Choose an appropriate risk level:
- low: reversible or low-impact action
- medium: modifies workload or service configuration
- high: potentially disruptive action

Return the remediation plan using the required structured format.
"""
            ),
            HumanMessage(
                content=f"""
Resource type: {state["resource_type"]}
Resource name: {state["resource_name"]}
Namespace: {state["namespace"]}

Diagnosis:
{state["diagnosis"]}
"""
            ),
        ]
    )

    state["remediation_plan"] = cast(RemediationPlan, response)

    return state


SUPPORTED_ACTIONS = {
    "restart_deployment",
    "scale_deployment",
    "update_deployment_image",
    "update_deployment_command",
    "update_service_selector",
}


def validate_remediation_plan_node(
    state: RemediationState,
) -> RemediationState:
    """
    Validate that the remediation plan is supported and has
    the required parameters.
    """

    plan = state["remediation_plan"]

    if plan is None:
        state["plan_valid"] = False
        state["validation_error"] = "No remediation plan was generated."
        return state

    # 1. Check supported action
    if plan.action not in SUPPORTED_ACTIONS:
        state["plan_valid"] = False
        state["validation_error"] = (
            f"Unsupported remediation action: {plan.action}"
        )
        return state

    # 2. Ensure target matches the original request/context
    if (
        plan.target.resource_type != state["resource_type"]
        or plan.target.resource_name != state["resource_name"]
        or plan.target.namespace != state["namespace"]
    ):
        state["plan_valid"] = False
        state["validation_error"] = (
            "Remediation plan target does not match the diagnosed resource."
        )
        return state

    # 3. Validate action-specific parameters
    parameters = plan.parameters

    if plan.action == "scale_deployment":
        replicas = parameters.get("replicas")

        if not isinstance(replicas, int) or replicas < 0:
            state["plan_valid"] = False
            state["validation_error"] = (
                "scale_deployment requires a non-negative integer 'replicas'."
            )
            return state

    elif plan.action == "update_deployment_image":
        image = parameters.get("image")

        if not isinstance(image, str) or not image.strip():
            state["plan_valid"] = False
            state["validation_error"] = (
                "update_deployment_image requires a valid 'image'."
            )
            return state

    elif plan.action == "update_deployment_command":
        command = parameters.get("command")

        if (
            not isinstance(command, list)
            or not command
            or not all(isinstance(item, str) for item in command)
        ):
            state["plan_valid"] = False
            state["validation_error"] = (
                "update_deployment_command requires a non-empty "
                "list of string values in 'command'."
            )
            return state

    elif plan.action == "update_service_selector":
        selector = parameters.get("selector")

        if (
            not isinstance(selector, dict)
            or not selector
            or not all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in selector.items()
            )
        ):
            state["plan_valid"] = False
            state["validation_error"] = (
                "update_service_selector requires a non-empty "
                "string-to-string 'selector' dictionary."
            )
            return state

    # restart_deployment requires no parameters
    state["plan_valid"] = True
    state["validation_error"] = None

    return state


def approval_gate_node(
    state: RemediationState,
) -> RemediationState:
    """
    Pause the remediation workflow and wait for user approval.
    """

    plan = state["remediation_plan"]

    if plan is None:
        state["approved"] = False
        return state

    approval_response = interrupt(
        {
            "type": "remediation_approval",
            "message": "Approve this remediation action?",
            "plan": plan.model_dump(),
        }
    )

    state["approved"] = approval_response["approved"]

    return state