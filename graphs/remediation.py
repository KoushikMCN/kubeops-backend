from langgraph.graph import START, END, StateGraph

from graphs.nodes.remediation_nodes import (
    create_remediation_plan_node,
    validate_remediation_plan_node,
)
from state.remediation_state import RemediationState


def route_after_validation(
    state: RemediationState,
) -> str:
    """
    Route based on whether the remediation plan is valid.
    """

    if state["plan_valid"]:
        return "approval_pending"

    return "invalid_plan"


def build_remediation_graph():
    """
    Build the Kubernetes remediation workflow.
    """

    graph = StateGraph(RemediationState)

    graph.add_node(
        "create_remediation_plan",
        create_remediation_plan_node,
    )

    graph.add_node(
        "validate_remediation_plan",
        validate_remediation_plan_node,
    )

    graph.add_edge(
        START,
        "create_remediation_plan",
    )

    graph.add_edge(
        "create_remediation_plan",
        "validate_remediation_plan",
    )

    graph.add_conditional_edges(
        "validate_remediation_plan",
        route_after_validation,
        {
            "invalid_plan": END,
            "approval_pending": END,
        },
    )

    return graph.compile()